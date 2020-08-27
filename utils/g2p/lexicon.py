import locale
import re
from collections import defaultdict

# set of phonemes used in Mary TTS German lexicon, excluding length markers
marytts_phonemes = [
    "@", "2", "6", "9", "a", "a~", "aI", "aU", "b", "C", "d", "D", "e", "e~",
    "E", "EI", "f", "g", "h", "i", "I", "j", "k", "l", "m", "n", "N", "o",
    "o~", "O", "OY", "p", "pf", "r", "R", "s", "S", "t", "T", "ts", "tS", "u",
    "U", "v", "w", "x", "y", "Y", "z", "Z"
]
marytts_to_ipa = { 
    "@":"ə", "2":"ø", "6":"ɐ", "9":"œ", "a":"a", "a~":"ã", "aI":"aɪ",
    "aU":"aʊ", "b":"b", "C":"ç", "d":"d", "D":"ð", "e":"e", "e~":"ẽ", "E":"ɛ",
    "EI":"ɛɪ", "f":"f", "g":"ɡ", "h":"h", "i":"i", "I":"ɪ", "j":"j", "k":"k",
    "l":"l", "m":"m", "n":"n", "N":"ŋ", "o":"o", "o~":"õ", "O":"ɔ", "OY":"ɔʏ",
    "p":"p", "pf":"pf", "r":"r", "R":"ʀ", "s":"s", "S":"ʃ", "t":"t", "T":"θ",
    "ts":"ts", "tS":"tʃ", "u":"u", "U":"ʊ", "v":"v", "w":"w", "x":"x", "y":"y",
    "Y":"ʏ", "z":"z", "Z":"ʒ"
}

def preprocess_marytts(lex_in, lex_out, phone_map):
    """Convert Mary TTS German lexicon to standard format."""
    with open(lex_in) as inf, open(lex_out, 'w') as outf:
        lexicon = defaultdict(set)
        # remove stress, length, syllable boundaries and glottal stops
        strip_chars = re.compile("[',:\-?]")
        multi_space = re.compile(" +")
        for line in inf:
            # skip strange Greek character entries
            if line.startswith(('α', 'β', 'γ')):
                continue
            word, pron = line.strip().split('|')
            word = word.lower()
            pron = re.sub(strip_chars, '', pron)
            pron = re.sub(multi_space, ' ', pron)
            pron = pron.strip()
            lexicon[word].add(pron)
        # TODO: Find some way to sort entries according to German rules,
        # e.g. with <ä> after <a> and not after <z>. Is there a way to do
        # that which doesn't rely on having de_DE.utf-8 locale generated
        # on the host (Linux) machine and set as current LC_COLLATE?
        for word in sorted(lexicon.keys()):
            for pron in lexicon[word]:
                pron = ' '.join(phone_map[p] for p in pron.split(' '))
                outf.write("{}\t{}\n".format(word, pron))

