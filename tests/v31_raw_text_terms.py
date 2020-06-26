import sys
sys.path.append('..')

import spacy
from datetime import datetime
from spacy_to_naf import text_to_NAF, NAF_to_string

nlp = spacy.load('en_core_web_sm')

naf = text_to_NAF('He gave up.',
                   nlp,
                   dct=datetime.now(),
                   layers={'raw', 'text', 'terms'},
                   naf_version='v3.1',
                   layer_to_attributes_to_ignore={'terms' : {'morphofeat', 'type'}},
                   dtd_validation=True)

print(NAF_to_string(naf))
