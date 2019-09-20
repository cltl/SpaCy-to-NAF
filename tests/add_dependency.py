import sys
sys.path.append('..')

import spacy
from lxml import etree
from spacy_to_naf import text_to_NAF, NAF_to_string
from spacy_to_naf import EntityElement, add_entity_element
from datetime import datetime

nlp = spacy.load('en_core_web_sm')


NAF = text_to_NAF('The man saw the bird. The woman gave the gift to the person.',
                  nlp,
                  dct=datetime.now(),
                  layers={'raw', 'text', 'terms', 'deps'},
                  replace_hidden_characters=True,
                  map_udpos2naf_pos=True) # map UD pos to NAF pos


print(NAF_to_string(NAF))

