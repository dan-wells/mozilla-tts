# -*- coding: utf-8 -*-
"""
Define mappings from phonemes to SPE-style binary phonological feature vectors.
"""

from collections import namedtuple

# TODO: Consider adding support for diacritic feature vectors, e.g.
#   - velarization = [+high, +back]
#   - nasalization = [+nasal]
#   - aspiration = [+subglottal_pressure]
# Need to be able to add feature vectors so that result gives union of
# specified feature values. Default value for all other features in diacritic
# vectors should be set to 0. Then could be nicer to start handling things from
# multi-character plain ASCII symbols, rather than worry about fiddly IPA
# diacritic encoding.

spe_features = [
    'consonantal', 'sonorant', 'syllabic', 'round', 'coronal', 'anterior',
    'high', 'low', 'front', 'back', 'tense', 'voice', 'subglottal_pressure',
    'constricted_glottis', 'continuant', 'strident', 'lateral',
    'delayed_release', 'nasal', 'space', 'eos', 'question', 'excl', 'punc'
]
SPEFeatures = namedtuple('SPEFeatures', spe_features)
spe_feature_map = {
    ' ': SPEFeatures(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0),
    '.': SPEFeatures(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
    '?': SPEFeatures(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0),
    '!': SPEFeatures(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0),
    ',': SPEFeatures(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1),
    't': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    'd': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
    's': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0),
    'z': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0),
    'ɬ': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0),
    'ɮ': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0),
    'θ': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
    'ð': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʃ': SPEFeatures(1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0),
    'ʒ': SPEFeatures(1,0,0,0,1,0,1,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0),
    'c': SPEFeatures(1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    'ɟ': SPEFeatures(1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
    'ç': SPEFeatures(1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʝ': SPEFeatures(1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɕ': SPEFeatures(1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0),
    'ʑ': SPEFeatures(1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0),
    'p': SPEFeatures(1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    'b': SPEFeatures(1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
    'f': SPEFeatures(1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0),
    'v': SPEFeatures(1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0),
    'ɸ': SPEFeatures(1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
    'β': SPEFeatures(1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'k': SPEFeatures(1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    'g': SPEFeatures(1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
    'ɡ': SPEFeatures(1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
    'x': SPEFeatures(1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɣ': SPEFeatures(1,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'q': SPEFeatures(1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    'ɢ': SPEFeatures(1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
    'χ': SPEFeatures(1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0),
    'ʁ': SPEFeatures(1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0),
    'ħ': SPEFeatures(1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʕ': SPEFeatures(1,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'h': SPEFeatures(0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɦ': SPEFeatures(0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʔ': SPEFeatures(0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0),
    'm': SPEFeatures(1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0),
    'ṃ': SPEFeatures(1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0),
    'n': SPEFeatures(1,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0),
    'ṇ': SPEFeatures(1,1,1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0),
    'ŋ': SPEFeatures(1,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0),
    'ɲ': SPEFeatures(1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0),
    'ɴ': SPEFeatures(1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0),
    'l': SPEFeatures(1,1,0,0,1,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0),
    'ḷ': SPEFeatures(1,1,1,0,1,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0),
    'ɫ': SPEFeatures(1,1,0,0,1,1,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0),
    'ʎ': SPEFeatures(1,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0),
    'r': SPEFeatures(1,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0),
    'ɹ': SPEFeatures(1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɾ': SPEFeatures(1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
    'ʀ': SPEFeatures(1,1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0),
    'j': SPEFeatures(0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'w': SPEFeatures(0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʍ': SPEFeatures(0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɥ': SPEFeatures(0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɰ': SPEFeatures(0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'i': SPEFeatures(0,1,1,0,0,0,1,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɪ': SPEFeatures(0,1,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'y': SPEFeatures(0,1,1,1,0,0,1,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʏ': SPEFeatures(0,1,1,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ᵻ': SPEFeatures(0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɨ': SPEFeatures(0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʉ': SPEFeatures(0,1,1,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'u': SPEFeatures(0,1,1,1,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʊ': SPEFeatures(0,1,1,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɯ': SPEFeatures(0,1,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'e': SPEFeatures(0,1,1,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ẽ': SPEFeatures(0,1,1,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,1,0,0,0,0,0),
    'ɛ': SPEFeatures(0,1,1,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ø': SPEFeatures(0,1,1,1,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'œ': SPEFeatures(0,1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'o': SPEFeatures(0,1,1,1,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'õ': SPEFeatures(0,1,1,1,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,0,0,0,0,0),
    'ɤ': SPEFeatures(0,1,1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɔ': SPEFeatures(0,1,1,1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ʌ': SPEFeatures(0,1,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɐ': SPEFeatures(0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɒ': SPEFeatures(0,1,1,1,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɑ': SPEFeatures(0,1,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'æ': SPEFeatures(0,1,1,0,0,0,0,1,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'a': SPEFeatures(0,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ã': SPEFeatures(0,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0),
    'ə': SPEFeatures(0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'ɜ': SPEFeatures(0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
    'tʃ': SPEFeatures(1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0),
    'dʒ': SPEFeatures(1,0,0,0,1,0,1,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0),
    'ts': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0),
    'dz': SPEFeatures(1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0),
    'kx': SPEFeatures(1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0),
    'pf': SPEFeatures(1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0),
    'ɚ': (SPEFeatures(0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0),
          SPEFeatures(1,1,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0)),
}

class PhonologicalFeatureVector(object):
    """Set of phonological features characterizing a phoneme."""
    def __init__(self, phoneme, feature_map):
        self.phoneme = phoneme
        self.features = feature_map[phoneme]

    def __eq__(self, other):
        return self.features == other.features

    def __len__(self):
        return len(self.features)

    def __repr__(self):
        return "/{}/, {}".format(self.phoneme, self.features)

def phoneme_to_feature(phonemes, feature_map):
    skip_chars = "ˈˌːˑ" # IPA stress and length diacritics from phonemize
    features = []
    for char in phonemes:
        try:
            # maps to /@r/ sequence in spe_feature_map
            if char == 'ɚ':
                features.extend(feature_map[char])
            else:
                features.append(feature_map[char])
        except KeyError:
            if char not in skip_chars:
                print(" > WARNING: no mapping defined from character '{}' "
                      "to feature vector. Skipping.".format(char))
            continue
    return features
