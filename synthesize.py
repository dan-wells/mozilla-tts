# pylint: disable=redefined-outer-name, unused-argument
import os
import time
import argparse
import torch
import json
import string

from TTS.utils.synthesis import synthesis
from TTS.utils.generic_utils import setup_model
from TTS.utils.g2p import load_g2p, train_g2p
from TTS.utils.g2p.lexicon import preprocess_lexicon
from TTS.utils.html import make_audio_page
from TTS.utils.io import load_config
from TTS.utils.text.features import spe_features
from TTS.utils.text.symbols import make_symbols, symbols, phonemes
from TTS.utils.audio import AudioProcessor


def tts(model,
        vocoder_model,
        C,
        VC,
        text,
        ap,
        ap_vocoder,
        use_cuda,
        batched_vocoder,
        speaker_id=None,
        text_format='text',
        figures=False):
    t_1 = time.time()
    use_vocoder_model = vocoder_model is not None
    waveform, alignment, _, postnet_output, stop_tokens, _ = synthesis(
        model, text, C, use_cuda, ap, speaker_id, style_wav=False,
        truncated=False, enable_eos_bos_chars=C.enable_eos_bos_chars,
        use_griffin_lim=(not use_vocoder_model), do_trim_silence=True,
        text_format=text_format)

    if C.model == "Tacotron" and use_vocoder_model:
        postnet_output = ap.out_linear_to_mel(postnet_output.T).T
    # correct if there is a scale difference b/w two models
    if use_vocoder_model:
        postnet_output = ap._denormalize(postnet_output)
        postnet_output = ap_vocoder._normalize(postnet_output)
        vocoder_input = torch.FloatTensor(postnet_output.T).unsqueeze(0)
        waveform = vocoder_model.generate(
            vocoder_input.cuda() if use_cuda else vocoder_input,
            batched=batched_vocoder,
            target=8000,
            overlap=400)
    print(" >  Run-time: {}".format(time.time() - t_1))
    return alignment, postnet_output, stop_tokens, waveform


if __name__ == "__main__":

    global symbols, phonemes

    parser = argparse.ArgumentParser()
    parser.add_argument('text', type=str, help='Text to generate speech, or file containing multiple utterances.')
    parser.add_argument('config_path',
                        type=str,
                        help='Path to model config file.')
    parser.add_argument(
        'model_path',
        type=str,
        help='Path to model file.',
    )
    parser.add_argument(
        'out_path',
        type=str,
        help='Path to save final wav file. Wav file will be names as the text given.',
    )
    parser.add_argument('--use_cuda',
                        type=bool,
                        help='Run model on CUDA.',
                        default=False)
    parser.add_argument(
        '--vocoder_path',
        type=str,
        help=
        'Path to vocoder model file. If it is not defined, model uses GL as vocoder. Please make sure that you installed vocoder library before (WaveRNN).',
        default="",
    )
    parser.add_argument('--vocoder_config_path',
                        type=str,
                        help='Path to vocoder model config file.',
                        default="")
    parser.add_argument(
        '--batched_vocoder',
        type=bool,
        help="If True, vocoder model uses faster batch processing.",
        default=True)
    parser.add_argument('--speakers_json',
                        type=str,
                        help="JSON file for multi-speaker model.",
                        default="")
    parser.add_argument(
        '--speaker_id',
        type=int,
        help="target speaker_id if the model is multi-speaker.",
        default=None)
    parser.add_argument(
        '--text_format',
        type=str,
        help="Symbols used for input texts, either `text` or `phoneme`.",
        choices=["text", "phoneme"],
        default="text")
    parser.add_argument(
        '--html_audio_page',
        type=str,
        help="File to write html for playing generated audio files.",
        default="")
    args = parser.parse_args()

    if args.vocoder_path != "":
        assert args.use_cuda, " [!] Enable cuda for vocoder."
        from WaveRNN.models.wavernn import Model as VocoderModel

    # load the config
    C = load_config(args.config_path)
    C.forward_attn_mask = True

    # load the audio processor
    ap = AudioProcessor(**C.audio)

    # if the vocabulary was passed, replace the default
    if 'characters' in C.keys():
        symbols, phonemes = make_symbols(**C.characters)

    # load speakers
    if args.speakers_json != '':
        speakers = json.load(open(args.speakers_json, 'r'))
        num_speakers = len(speakers)
    else:
        num_speakers = 0

    # load the model
    if C.use_features:
        num_chars = len(spe_features)
    elif C.use_phonemes:
        num_chars = len(phonemes)
    else:
        num_chars = len(symbols)
    if C.g2p['method'] == 'phonetisaurus':
        preprocess_lexicon(C.g2p)
        C.g2p['model_path'] = os.path.join(C.g2p['train_dir'], "{}.fst".format(C.g2p['model_prefix']))
        C.g2p['g2p_tester'] = load_g2p(C.g2p['model_path'], lexicon=C.g2p['lexicon_path'])
    model = setup_model(num_chars, num_speakers, C)
    cp = torch.load(args.model_path)
    model.load_state_dict(cp['model'])
    model.eval()
    if args.use_cuda:
        model.cuda()
    model.decoder.set_r(cp['r'])

    # load vocoder model
    if args.vocoder_path != "":
        VC = load_config(args.vocoder_config_path)
        ap_vocoder = AudioProcessor(**VC.audio)
        bits = 10
        vocoder_model = VocoderModel(rnn_dims=512,
                                     fc_dims=512,
                                     mode=VC.mode,
                                     mulaw=VC.mulaw,
                                     pad=VC.pad,
                                     upsample_factors=VC.upsample_factors,
                                     feat_dims=VC.audio["num_mels"],
                                     compute_dims=128,
                                     res_out_dims=128,
                                     res_blocks=10,
                                     hop_length=ap.hop_length,
                                     sample_rate=ap.sample_rate,
                                     use_aux_net=True,
                                     use_upsample_net=True)

        check = torch.load(args.vocoder_path)
        vocoder_model.load_state_dict(check['model'])
        vocoder_model.eval()
        if args.use_cuda:
            vocoder_model.cuda()
    else:
        vocoder_model = None
        VC = None
        ap_vocoder = None

    # get input texts
    if os.path.isfile(args.text):
        with open(args.text) as text_lines:
            texts = [i.strip() for i in text_lines.readlines()]
    else:
        texts = [args.text]

    if args.html_audio_page:
        wavs = []

    # synthesize voice
    for n_audio, text in enumerate(texts):
        print(" > Text: {}".format(text))
        _, _, _, wav = tts(model,
                           vocoder_model,
                           C,
                           VC,
                           text,
                           ap,
                           ap_vocoder,
                           args.use_cuda,
                           args.batched_vocoder,
                           speaker_id=args.speaker_id,
                           text_format=args.text_format,
                           figures=False)

        # save the results
        if args.text_format == 'text':
            file_name = text.replace(" ", "_")
            file_name = file_name.translate(
                str.maketrans('', '', string.punctuation.replace('_', ''))) + '.wav'
        else:
            file_name = 'SynthAudio{:04d}.wav'.format(n_audio)
        if not os.path.exists(args.out_path):
            os.makedirs(args.out_path)
        out_path = os.path.join(args.out_path, file_name)
        print(" > Saving output to {}".format(out_path))
        ap.save_wav(wav, out_path)
        if args.html_audio_page:
            wavs.append(out_path)

    # write html audio page
    if args.html_audio_page:
        make_audio_page(audios=wavs, transcripts=texts, html_out=args.html_audio_page)

