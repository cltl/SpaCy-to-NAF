import sys
sys.path.append('..')

import spacy
from lxml import etree
from spacy_to_naf import text_to_NAF, NAF_to_string
from spacy_to_naf import EntityElement, add_entity_element
from spacy_to_naf import time_in_correct_format
from spacy_to_naf import add_linguisticProcessors_el
from datetime import datetime

nlp = spacy.load('en_core_web_sm')
naf_version = 'v4'
now = datetime.now()

tree = text_to_NAF('Tom Cruise is an actor.\n\n\nHe likes to act.',
                   nlp,
                   dct=now,
                   naf_version='v4',
                   layers={'raw', 'text', 'terms'},
                   replace_hidden_characters=True,
                   map_udpos2naf_pos=False,
                   dtd_validation=True) # map UD pos to NAF pos

root = tree.getroot()
naf_header = root.find('nafHeader')
time_as_string = time_in_correct_format(now)

modelname = 'Wikipedia hyperlinks'
add_linguisticProcessors_el(naf_header,
                            layer='entities',
                            start_time=time_as_string,
                            end_time=time_as_string,
                            modelname=modelname)


entities_layer = root.find('entities')
if entities_layer is None:
    etree.SubElement(root, "entities")
    entities_layer = root.find('entities')

entity_data = EntityElement(eid='1',
                            entity_type='None',
                            targets=['t1', 't2'],
                            text='Tom Cruise',
                            ext_refs=[{'reference' : 'https://en.wikipedia.org/wiki/Tom_Cruise',
                                       'resource' : 'https://www.wikipedia.org/',
                                       'source' : 'Wikipedia hyperlinks',
                                       'timestamp' : time_as_string}])

add_entity_element(entities_layer,
                   naf_version,
                   entity_data)

print(NAF_to_string(root))

