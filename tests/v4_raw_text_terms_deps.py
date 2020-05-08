import sys
sys.path.append('..')

import spacy
from datetime import datetime
from spacy_to_naf import text_to_NAF, NAF_to_string

nlp = spacy.load('nl_core_news_sm')

naf = text_to_NAF('De aanslagpleger nam het document aan.',
                   nlp,
                   dct=datetime.now(),
                   layers={'raw', 'text', 'terms', 'deps'},
                   naf_version='v4',
                   layer_to_attributes_to_ignore={'terms' : {'morphofeat', 'type'}},
                   replace_hidden_characters=True,
                   dtd_validation=True)

print(NAF_to_string(naf))