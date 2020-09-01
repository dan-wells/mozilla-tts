# -*- coding: utf-8 -*-

import locale
import os
import re
import sys
from collections import defaultdict

def preprocess_lexicon(g2p_config):
    lex_in = g2p_config['lexicon_path']
    train_dir = g2p_config['train_dir']
    lex_out = os.path.join(train_dir, '{}.lex'.format(g2p_config['model_prefix']))
    preprocessor = get_lexicon_preprocessor_by_name(g2p_config['lexicon'])
    phonemap = get_lexicon_phonemap_by_name(g2p_config['lexicon'])
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    preprocessor(lex_in, lex_out, phonemap)
    g2p_config['lexicon_path'] = lex_out

def get_lexicon_preprocessor_by_name(name):
    """Returns the respective preprocessing function."""
    thismodule = sys.modules[__name__]
    return getattr(thismodule, "preprocess_{}".format(name.lower()))

def get_lexicon_phonemap_by_name(name):
    """Returns the respective lexicon-to-IPA symbol map."""
    thismodule = sys.modules[__name__]
    return getattr(thismodule, "{}_to_ipa".format(name.lower()))

# set of phonemes used in Mary TTS German lexicon, excluding length markers
marytts_de_phonemes = [
    "@", "2", "6", "9", "a", "a~", "aI", "aU", "b", "C", "d", "D", "e", "e~",
    "E", "EI", "f", "g", "h", "i", "I", "j", "k", "l", "m", "n", "N", "o",
    "o~", "O", "OY", "p", "pf", "r", "R", "s", "S", "t", "T", "ts", "tS", "u",
    "U", "v", "w", "x", "y", "Y", "z", "Z"
]
marytts_de_to_ipa = {
    "@":"ə", "2":"ø", "6":"ɐ", "9":"œ", "a":"a", "a~":"ã", "aI":"aɪ",
    "aU":"aʊ", "b":"b", "C":"ç", "d":"d", "D":"ð", "e":"e", "e~":"ẽ", "E":"ɛ",
    "EI":"ɛɪ", "f":"f", "g":"ɡ", "h":"h", "i":"i", "I":"ɪ", "j":"j", "k":"k",
    "l":"l", "m":"m", "n":"n", "N":"ŋ", "o":"o", "o~":"õ", "O":"ɔ", "OY":"ɔʏ",
    "p":"p", "pf":"pf", "r":"ɹ", "R":"ʀ", "s":"s", "S":"ʃ", "t":"t", "T":"θ",
    "ts":"ts", "tS":"tʃ", "u":"u", "U":"ʊ", "v":"v", "w":"w", "x":"x", "y":"y",
    "Y":"ʏ", "z":"z", "Z":"ʒ"
}

def preprocess_marytts_de(lex_in, lex_out, phone_map):
    """Convert Mary TTS lexicon file to standard format."""
    with open(lex_in) as inf, open(lex_out, 'w') as outf:
        # remove stress, length, syllable boundaries and glottal stops
        strip_chars = re.compile("[',:\-?]")
        multi_space = re.compile(" +")
        for line in inf:
            # skip strange Greek character entries
            if line.startswith(('α', 'β', 'γ')):
                continue
            word, pron = line.strip().split('|')
            word = word.lower()
            # some abbreviations tend to confuse g2p training
            if word.endswith("'"):
                word = word.strip("'")
            pron = re.sub(strip_chars, '', pron)
            pron = re.sub(multi_space, ' ', pron)
            pron = pron.strip()
            pron = ' '.join(phone_map[p] for p in pron.split(' '))
            outf.write("{}\t{}\n".format(word, pron))

# set of phonemes used in Combilex surface lexicons
combilex_phonemes = [
    'A', 'a', 'aI', 'aU', 'E', 'eI', 'E@', '@U', 'Q', 'O', 'OI', '3', '@', 'I',
    'i', 'I@', 'U', 'V', 'u', 'U@', 'N', 'T', 'D', 'S', 'Z', 'tS', 'dZ', 'm=',
    'n=', 'l=', 'e~', 'o~', 'j', 'w', '4', '5', 'b', 'd', 'f', 'g', 'h', 'k',
    'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'z'
]

combilex_to_ipa = {
    'A':'ɑ', 'a':'a', 'aI':'aɪ', 'aU':'aʊ', 'E':'ɛ', 'eI':'eɪ', 'E@':'ɛə',
    '@U':'əʊ', 'Q':'ɒ', 'O':'ɔ', 'OI':'ɔɪ', '3':'ɜ', '@':'ə', 'I':'ɪ', 'i':'i',
    'I@':'ɪə', 'U':'ʊ', 'V':'ʌ', 'u':'u', 'U@':'ʊə', 'N':'ŋ', 'T':'θ', 'D':'ð',
    'S':'ʃ', 'Z':'ʒ', 'tS':'tʃ', 'dZ':'dʒ', 'm=':'ṃ', 'n=':'ṇ', 'l=':'ḷ',
    'e~':'ẽ', 'o~':'õ', 'j':'j', 'w':'w', '4':'ɾ', '5':'ɫ', 'b':'b', 'd':'d',
    'f':'f', 'g':'ɡ', 'h':'h', 'k':'k', 'l':'l', 'm':'m', 'n':'n', 'p':'p',
    'r':'ɹ', 's':'s', 't':'t', 'v':'v', 'z':'z'
}

def parse_combilex_entry(line):
    """Parse Combilex entry and make named fields available."""
    combilexEntryFields_re = re.compile( r"""^(?P<hw>[^:]+):
                                              (?P<sense>[0-9]+):
                                              (?P<pos>[A-Z$/|]*):
                                              (?P<variant>[^:]*):
                                              (?P<pron>[^:]+):
                                              (?P<table>[a-z/]+):
                                              (?P<word_id>[0-9-]+):
                                              (?P<strength>[sw]?):
                                              (?P<pron_id>[0-9-]*):
                                              (?P<ref_id>[^:]*):
                                              (?P<derivation>[^:]*):
                                              (?P<lang>[a-z/]*):
                                              (?P<semantics>[^:]*):
                                              (?P<domain>[^:]*):
                                              (?P<fname>[y]?):
                                              (?P<fname_gender>[m/f]*):
                                              (?P<sname>[y]?):
                                              (?P<sname_gender>[m/f]*):
                                              (?P<country>(?:[A-Z][A-Z]/?)*):
                                              (?P<place_region>[^:]*):
                                              (?P<place_type>[^:]*)$""", re.VERBOSE )
    return combilexEntryFields_re.search( line )

def strip_combilex(pronstr):
    """Strip everything but phones from Combilex pron string."""
    strippat1 = re.compile( r'(?: [0+]_[^ ]+)|_[^ ]+|[<{>}]', re.UNICODE )
    strippat2 = re.compile( r',' )
    strippat3 = re.compile( r' # ' )
    strippat4 = re.compile( r' \. ' )
    strippat5 = re.compile( r' ?["%] ' )
    strippat6 = re.compile( r'`' ) # rhoticity marker always redundant with following /r/
    strippat7 = re.compile( r'0' ) # considered 'not redundant', but don't want them
    spacesqueezepat = re.compile( r' +' )

    pron =   strippat1.sub( '', pronstr )
    pron =   strippat2.sub( ' ', pron )
    pron =   strippat3.sub( ' ', pron )
    pron =   strippat4.sub( ' ', pron )
    pron =   strippat5.sub( ' ', pron )
    pron =   strippat6.sub( '', pron )
    pron =   strippat7.sub( '', pron )
    cleanpron =   spacesqueezepat.sub( ' ', pron )

    return cleanpron.strip()

def preprocess_combilex(lex_in, lex_out, phone_map):
    """Convert Combilex lexicon file to standard format."""
    with open(lex_in) as inf, open(lex_out, 'w') as outf:
        for line in inf:
            entry = parse_combilex_entry(line)
            word = entry.group('hw')
            word = word.lower()
            # skip multi-word entries, generally both words are also listed separately
            if ' ' in word:
                continue
            pron = entry.group('pron')
            pron = strip_combilex(pron)
            pron = ' '.join(phone_map[p] for p in pron.split(' '))
            outf.write("{}\t{}\n".format(word, pron))

