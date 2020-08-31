import tempfile
from TTS.utils.g2p.phonetisaurus_apply import G2PModelTester
from TTS.utils.g2p.phonetisaurus_train import G2PModelTrainer

def train_g2p(lexicon_file, model_out, g2p_dir):
    """Train G2P model from lexicon.

    Args:
        lexicon_file (str): Path to lexicon file. Head words should be
          separated from pronunciations by tabs, and pronunciations
          should be space-separated phoneme sequences.
        model_out (str): Prefix for final model name and intermediate
          training files. Final model will be called ${model_out}.fst
        g2p_dir (str): Directory to store final model and intermediate
          training files.
    """
    trainer = G2PModelTrainer(lexicon_file, model_prefix=model_out,
                              dir_prefix=g2p_dir, seq2_del=True)
    trainer.TrainG2PModel()


def load_g2p(model, lexicon=None):
    """Load trained G2P model from file.

    Args:
        model (str): Path to trained Phonetisaurus FST.
        lexicon (str): Path to optional reference lexicon.
    """
    tester = G2PModelTester(model, lexicon=lexicon) 
    return tester


def apply_g2p(text, tester):
    """Apply trained G2P model to text.

    Args:
        text (str): Words to convert to phonemes.
        model (obj): G2PModelTester object.
    """
    expected_punc = ['.', '?', '!', ',']
    # Phonetisaurus expects input from files one word per line
    with tempfile.NamedTemporaryFile(mode='w') as word_list:
        for c in text:
            if c in expected_punc:
                word_list.write("\n{}\n".format(c))
            elif c == ' ':
                word_list.write("\n{}\n".format(".space"))
            else:
                word_list.write(c)
        word_list.seek(0)
        phonemes = tester.ApplyG2PModel(word_list.name)
    return phonemes

