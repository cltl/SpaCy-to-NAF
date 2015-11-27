# coding: utf-8

from lxml import etree
from collections import namedtuple
from datetime import datetime

# Define Entity object:
Entity = namedtuple('Entity',['start', 'end', 'entity_type'])
WfElement = namedtuple('WfElement',['sent', 'wid', 'length', 'wordform', 'offset'])
TermElement = namedtuple('TermElement', ['tid', 'lemma', 'pos', 'morphofeat', 'targets', 'text'])
EntityElement = namedtuple('EntityElement', ['eid', 'entity_type', 'targets', 'text'])
DependencyRelation = namedtuple('DependencyRelation', ['from_term', 'to_term', 'rfunc', 'from_orth', 'to_orth'])

def normalize_token_orth(orth):
    if orth == '\n':
        return 'NEWLINE'
    else:
        return orth

def get_entity_type(span):
    "Function to get the entity type of an entity span."
    ent_type_set = {tok.ent_type_ for tok in span if tok.ent_type_ != ''}
    return ent_type_set.pop()

def entities(doc):
    "Generator that returns Entity objects for a given document."
    for ent in doc.ents:
        yield Entity(start = ent.start,
                     end = ent.end -1,
                     entity_type = get_entity_type(ent))

def add_wf_element(text_layer, wf_data):
    """
    Function that adds a wf element to the text layer.
    """
    wf_el = etree.SubElement(text_layer, "wf")
    wf_el.set("sent", wf_data.sent)
    wf_el.set("id", wf_data.wid)
    wf_el.set("length", wf_data.length)
    wf_el.set("offset", wf_data.offset)
    wf_el.text = wf_data.wordform

def add_term_element(terms_layer, term_data):
    """
    Function that adds a term element to the text layer.
    """
    term_el = etree.SubElement(terms_layer, "term")
    term_el.set("id", term_data.tid)
    term_el.set("lemma", term_data.lemma)
    term_el.set("pos", term_data.pos)
    term_el.set("morphofeat", term_data.morphofeat)
    span = etree.SubElement(term_el, "span")
    span.append(etree.Comment(' '.join(term_data.text)))
    for target in term_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)

def add_entity_element(entities_layer, entity_data):
    """
    Function that adds an entity element to the entity layer.
    """
    entity_el = etree.SubElement(entities_layer, "entity")
    entity_el.set("id", entity_data.eid)
    entity_el.set("type", entity_data.entity_type)
    references_el = etree.SubElement(entity_el, "references")
    span = etree.SubElement(references_el, "span")
    span.append(etree.Comment(' '.join(entity_data.text)))
    for target in entity_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)

def add_dependency_element(dependency_layer, dep_data):
    """
    Function that adds dependency elements to the deps layer.
    """
    comment = dep_data.rfunc + '(' + dep_data.from_orth + ',' + dep_data.to_orth + ')'
    dependency_layer.append(etree.Comment(comment))
    dep_el = etree.SubElement(dependency_layer, "dep")
    dep_el.set("from", dep_data.from_term)
    dep_el.set("to", dep_data.to_term)
    dep_el.set("rfunc", dep_data.rfunc)

def dependencies_to_add(token):
    """
    Walk up the tree, creating a DependencyRelation for each label.
    The relation is then passed to the
    """
    deps = []
    while token.head is not token:
        dep_data = DependencyRelation(from_term = 't' + str(token.head.i),
                                      to_term = 't' + str(token.i),
                                      rfunc = token.dep_,
                                      from_orth = normalize_token_orth(token.head.orth_),
                                      to_orth = normalize_token_orth(token.orth_))
        deps.append(dep_data)
        token = token.head
    return deps
    
def naf_from_doc(doc, time=None):
    """
    Function that takes a document and returns an ElementTree
    object that corresponds to the root of the NAF structure.
    """
    # NAF:
    # ---------------------
    # Create NAF root.
    root = etree.Element("NAF")
    
    # Create text and terms layers.
    naf_header = etree.SubElement(root, "nafHeader")
    
    ling_proc = etree.SubElement(naf_header, "linguisticProcessors")
    ling_proc.set("layer", "text")
    lp = etree.SubElement(ling_proc, "lp")
    lp.set("name", "SpaCy")
    if time:
        lp.set("timestamp", time)
    
    ling_proc = etree.SubElement(naf_header, "linguisticProcessors")
    lp = etree.SubElement(ling_proc, "lp")
    lp.set("name", "SpaCy")
    if time:
        lp.set("timestamp", time)
    ling_proc.set("layer", "terms")
    
    text_layer = etree.SubElement(root, "text")
    terms_layer = etree.SubElement(root, "terms")
    entities_layer = etree.SubElement(root, "entities")
    dependency_layer = etree.SubElement(root, "deps")
    
    # Initialize variables:
    # ---------------------
    # - Use a generator for entity awareness.
    entity_gen = entities(doc)
    next_entity = next(entity_gen)
    
    # - Bookkeeping variables.
    current_term = []    # Use a list for multiword expressions.
    current_term_orth = [] # id.
    
    current_entity = []    # Use a list for multiword entities.
    current_entity_orth = [] # id.
    
    current_token = 0    # Keep track of the token number.
    term_number = 0      # Keep track of the term number.
    entity_number = 0    # Keep track of the entity number.
    
    parsing_entity = False # State change: are we working on a term or not?
    
    
    for sentence_number, sentence in enumerate(doc.sents, start = 1):
        dependencies_for_sentence = []
        for token_number, token in enumerate(sentence, start = current_token):
            # Do we need a state change?
            if token_number == next_entity.start:
                parsing_entity = True
            
            wid = 'w' + str(token_number)
            tid = 't' + str(term_number)
            
            current_term.append(wid)
            current_term_orth.append(normalize_token_orth(token.orth_))
            
            if parsing_entity:
                current_entity.append(tid)
                current_entity_orth.append(normalize_token_orth(token.orth_))
            
            # Create WfElement data:
            wf_data = WfElement(sent = str(sentence_number),
                           wid = wid,
                           length = str(len(token.text)),
                           wordform = normalize_token_orth(token.text),
                           offset = str(token.idx))
            
            # Create TermElement data:
            term_data = TermElement(tid = tid,
                                    lemma = token.lemma_,
                                    pos = token.pos_,
                                    morphofeat = token.tag_,
                                    targets = current_term,
                                    text = current_term_orth)
            
            add_wf_element(text_layer, wf_data)
            add_term_element(terms_layer, term_data)
            
            # Move to the next term
            term_number += 1
            current_term = []
            current_term_orth = []
                
            if parsing_entity and token_number == next_entity.end:
                # Create new entity ID.
                eid = 'e' + str(entity_number)
                
                # Create Entity data:
                entity_data = EntityElement(eid = eid,
                                            entity_type = next_entity.entity_type,
                                            targets = current_entity,
                                            text = current_entity_orth)
                # Add data to XML:
                add_entity_element(entities_layer, entity_data)
                
                # Move to the next entity:
                entity_number += 1
                current_entity = []
                current_entity_orth = []
                
                # Move to the next entity
                parsing_entity = False
                try:
                    next_entity = next(entity_gen)
                except StopIteration:
                    # No more entities...
                    pass

            # Add dependencies for the current token to the list.
            for dep_data in dependencies_to_add(token):
                if not dep_data in dependencies_for_sentence:
                    dependencies_for_sentence.append(dep_data)

        # At the end of the sentence, add all the dependencies to the XML structure.
        for dep_data in dependencies_for_sentence:
            add_dependency_element(dependency_layer, dep_data)
        current_token = token_number + 1
    return root

def current_time():
    "Function that returns the current time (UTC)"
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SUTC")

def text_to_NAF(text, nlp):
    """
    Function that takes a text and returns an xml object containing the NAF.
    """
    doc = nlp(text)
    time = current_time()
    return naf_from_doc(doc, time=time)

def NAF_to_string(NAF, byte=False):
    """
    Function that takes an XML object containing NAF, and returns it as a string.
    If byte is True, then the output is a bytestring.
    """
    xml_string = etree.tostring(NAF, pretty_print=True, with_comments=True)
    if byte:
        return xml_string
    else:
        return xml_string.decode('utf-8')

# Command line functionality: given name of a file, process the file contents and
# print the NAF to stdout.
if __name__ == '__main__':
    import sys
    from spacy.en import English
    nlp = English()
    with open(sys.argv[1]) as f:
        text = f.read()
        NAF = text_to_NAF(text, nlp)
        print(NAF_to_string(NAF))
