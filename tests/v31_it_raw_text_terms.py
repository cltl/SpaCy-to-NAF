import sys
sys.path.append('..')

import spacy
from datetime import datetime
from spacy_to_naf import text_to_NAF, NAF_to_string


nlp = spacy.load('it_core_news_sm')

naf = text_to_NAF('Tom Cruise is an actor.\n\n\nHe likes to act.',
                   nlp,
                   dct=datetime.now(),
                   layers={'raw', 'text', 'terms'},
                   naf_version='v3.1',
                   layer_to_attributes_to_ignore={'terms' : {'morphofeat', 'type'}},
                   dtd_validation=True) # map UD pos to NAF pos
