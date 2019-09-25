import sys
sys.path.append('..')

import spacy
from lxml import etree
from spacy_to_naf import text_to_NAF, NAF_to_string
from spacy_to_naf import EntityElement, add_entity_element
from datetime import datetime

nlp = spacy.load('en_core_web_sm')


tree = text_to_NAF('Tom Cruise is an actor.\n\n\nHe likes to act.',
                   nlp,
                   dct=datetime.now(),
                   layers={'raw', 'text', 'terms'},
                   replace_hidden_characters=True,
                   map_udpos2naf_pos=True) # map UD pos to NAF pos

root = tree.getroot()


entities_layer = root.find('entities')
if entities_layer is None:
    etree.SubElement(root, "entities")
    entities_layer = root.find('entities')

entity_data = EntityElement(eid='1',
                            entity_type='None',
                            targets=['t1', 't2'],
                            text='Tom Cruise',
                            ext_refs=[{'reference' : 'https://en.wikipedia.org/wiki/Tom_Cruise',
                                       'resource' : 'Wikipedia'}])


add_entity_element(entities_layer, entity_data)

print(NAF_to_string(root))

