# coding: utf-8
import re
from lxml import etree
from collections import namedtuple
from datetime import datetime
import spacy
import io
import requests
import sys

def load_dtd_as_file_object(dtd_url, verbose=0):
    dtd = None
    r = requests.get(dtd_url)

    if r.status_code == 200:
        dtd_file_object = io.StringIO(r.text)
        dtd = etree.DTD(dtd_file_object)

    if verbose >= 1:
        print()
        if dtd is None:
            print(f'failed to load dtd from {dtd_url}')
        else:
            print(f'succesfully loaded dtd from {dtd_url}')

    return dtd

NAF_VERSION_TO_DTD = {
    'v3' : load_dtd_as_file_object('https://raw.githubusercontent.com/newsreader/NAF/master/naf.dtd'),
    'v3.1' : load_dtd_as_file_object('https://raw.githubusercontent.com/cltl/NAF-4-Development/master/res/naf_development/naf_v3.1.dtd')
}
# Define Entity object:
Entity = namedtuple('Entity',['start', 'end', 'entity_type'])
WfElement = namedtuple('WfElement',['sent', 'wid', 'length', 'wordform', 'offset'])
TermElement = namedtuple('TermElement', ['id', 'lemma', 'pos', 'type', 'morphofeat', 'targets', 'text'])
EntityElement = namedtuple('EntityElement', ['eid',
                                             'entity_type',
                                             'targets',
                                             'text',
                                             'ext_refs' # list of dictionaries, e.g., [{'reference' : 'Naples',
                                                                                      # 'resource' : 'Wikipedia'}]
                                             ])
DependencyRelation = namedtuple('DependencyRelation', ['from_term', 'to_term', 'rfunc', 'from_orth', 'to_orth'])
ChunkElement = namedtuple('ChunkElement', ['cid', 'head', 'phrase', 'text', 'targets'])

hidden_characters = [
    '\a',
    '\b',
    '\t',
    '\n',
    '\v',
    '\f',
    '\r',
]

hidden_table = {ord(hidden_character) : ' '
                for hidden_character in hidden_characters}

udpos2nafpos_info = {
    'ADJ' : {
        'class' : 'open',
        'naf_pos' : 'G'
    },
    'ADP' : {
        'class' : 'open',
        'naf_pos' : 'P'
    },
    'ADV' : {
        'class' : 'open',
        'naf_pos' : 'A'
    },
    'AUX' : {
        'class' : 'close',
        'naf_pos' : 'V',
    },
    'CCONJ' : {
        'class' : 'close',
        'naf_pos' : 'C'
    },
    'DET' : {
        'class' : 'close',
        'naf_pos' : 'D'
    },
    'INTJ' : {
        'class' : 'open',
        'naf_pos' : 'O'
    },
    'NOUN' : {
        'class' : 'open',
        'naf_pos' : 'N'
    },
    'NUM' : {
        'class' : 'close',
        'naf_pos' : 'O'
    },
    'PART' : {
        'class' : 'close',
        'naf_pos' : 'O'
    },
    'PRON' : {
        'class' : 'close',
        'naf_pos' : 'O'
    },
    'PROPN' : {
        'class' : 'open',
        'naf_pos' : 'R'
    },
    'PUNCT' : {
        'class' : 'close',
        'naf_pos' : 'O'
    },
    'SCONJ' : {
        'class' : 'close',
        'naf_pos' : 'O'
    },
    'SYM' : {
        'class' : 'open',
        'naf_pos' : 'O'
    },
    'VERB' : {
        'class' : 'open',
        'naf_pos' : 'V'
    },
    'X' : {
        'class' : 'open',
        'naf_pos' : 'O'
    },
    'SPACE' : {
        'class' : 'open',
        'naf_pos' : 'O'
    }
}


# Only allow legal strings in XML:
# http://stackoverflow.com/a/25920392/2899924
illegal_pattern = re.compile('[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+')
def remove_illegal_chars(text):
    return re.sub(illegal_pattern, '', text)


def normalize_token_orth(orth):
    if '\n' in orth:
       return 'NEWLINE'
    else:
        return remove_illegal_chars(orth)

def validate_naf_file(dtd, root):
    succes = dtd.validate(root)

    if not succes:
        print()
        print(sys.stderr.write("DTD error log:"))
        for error in dtd.error_log.filter_from_errors():
            sys.stderr.write(str(error))
        raise Exception(f'dtd validation failed. Please inspect stderr.')

    return succes

def create_seperable_verb_lemma(verb, particle, language):
    """joins components of a seperable verb"""
    if language == 'nl':
        lemma = particle+verb
    if language == 'en':
        lemma = f'{verb}_{particle}'
    return lemma

def get_mws_layer(root):
    mws_layer = root.find('multiwords')
    if mws_layer is None:
        etree.SubElement(root, 'multiwords')
        mws_layer = root.find('multiwords')
    return mws_layer

def get_next_mw_id(root):
    mws_layer = get_mws_layer(root)

    mw_ids = [int(mw_el.get('id')[2:])
              for mw_el in mws_layer.xpath('mw')]
    if mw_ids:
        next_mw_id = max(mw_ids) + 1
    else:
        next_mw_id = 1

    return f'mw{next_mw_id}'


def add_multi_words(root,
                    naf_version,
                    language):
    """
    Provided that the NAF file contains a
    adds multi-word terms to term layer in naf file
    """
    if naf_version == 'v3':
        print('add_multi_words function only applies to naf version 4')
        return root

    supported_languages = {'nl', 'en'}
    if language not in supported_languages:
        print(f'add_multi_words function only implemented for {supported_languages}, not for supplied {language}')
        return root

    # dictionary from tid -> term_el
    tid_to_term = {term_el.get('id') : term_el
                   for term_el in root.xpath('terms/term')}

    num_of_compound_prts = 0

    # loop deps el
    for dep in root.findall('deps/dep'):
        if dep.get('rfunc') == 'compound:prt':

            mws_layer = get_mws_layer(root)
            next_mw_id = get_next_mw_id(root)

            idverb = dep.get('from')
            idparticle = dep.get('to')
            num_of_compound_prts += 1

            verb_term_el = tid_to_term[idverb]
            verb = verb_term_el.get('lemma')
            verb_term_el.set('component_of', next_mw_id)

            particle_term_el = tid_to_term[idparticle]
            particle = particle_term_el.get('lemma')
            particle_term_el.set('component_of', next_mw_id)

            seperable_verb_lemma = create_seperable_verb_lemma(verb,
                                                               particle,
                                                               language)


            attributes = [('id', next_mw_id),
                          ('lemma', seperable_verb_lemma),
                          ('pos', 'VERB'),
                          ('type', 'phrasal')]

            mw_element = etree.SubElement(mws_layer,
                                          'mw')
            for attr, value in attributes:
                mw_element.set(attr, value)

            # add component elements
            components = [
                (f'{next_mw_id}.c1', idverb),
                (f'{next_mw_id}.c2', idparticle)
            ]
            for c_id, t_id in components:
                component = etree.SubElement(mw_element,
                                             'component',
                                              attrib={'id': c_id})
                span = etree.SubElement(component, 'span')
                etree.SubElement(span,
                                 'target',
                                 attrib={'id': t_id})

    return root

def prepare_comment_text(text):
    "Function to prepare text to be put inside a comment."
    text = text.replace('--','DOUBLEDASH')
    if text.endswith('-'):
        text = text[:-1] + 'SINGLEDASH'
    return text


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


def add_wf_element(text_layer, wf_data, cdata=True):
    """
    Function that adds a wf element to the text layer.
    """
    wf_el = etree.SubElement(text_layer, "wf")
    wf_el.set("sent", wf_data.sent)
    wf_el.set("id", wf_data.wid)
    wf_el.set("length", wf_data.length)
    wf_el.set("offset", wf_data.offset)

    if cdata:
        wf_el.text = etree.CDATA(wf_data.wordform)
    else:
        wf_el.text = wf_data.wordform


def add_term_element(terms_layer,
                     term_data,
                     unwanted_attributes=set(),
                     add_comments=False):
    """
    Function that adds a term element to the text layer.
    """
    term_el = etree.SubElement(terms_layer, "term")

    attrs = ['id', 'lemma', 'pos', 'type', 'morphofeat']

    for attr in attrs:
        if attr not in unwanted_attributes:
            term_el.set(attr, getattr(term_data, attr))

    span = etree.SubElement(term_el, "span")

    if add_comments:
        text = ' '.join(term_data.text)
        text = prepare_comment_text(text)
        span.append(etree.Comment(text))
    for target in term_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)

def add_entity_element(entities_layer,
                       naf_version,
                       entity_data,
                       add_comments=False):
    """
    Function that adds an entity element to the entity layer.
    """
    entity_el = etree.SubElement(entities_layer, "entity")
    entity_el.set("id", entity_data.eid)
    entity_el.set("type", entity_data.entity_type)

    if naf_version == 'v3':
        references_el = etree.SubElement(entity_el, "references")
        span = etree.SubElement(references_el, "span")
    elif naf_version == 'v3.1':
        span = etree.SubElement(entity_el, "span")

    if add_comments:
        text = ' '.join(entity_data.text)
        text = prepare_comment_text(text)
        span.append(etree.Comment(text))
    for target in entity_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)

    assert type(entity_data.ext_refs) == list, f'ext_refs should be a list of dictionaries (can be empty)'
    ext_refs_el = etree.SubElement(entity_el, 'externalReferences')
    for ext_ref_info in entity_data.ext_refs:
        one_ext_ref_el = etree.SubElement(ext_refs_el, 'externalRef')
        one_ext_ref_el.set('reference', ext_ref_info['reference'])

        for optional_attr in ['resource', 'source', 'timestamp']:
            if optional_attr in ext_ref_info:
                one_ext_ref_el.set(optional_attr, ext_ref_info[optional_attr])

def chunks_for_doc(doc):
    """
    Generator function that yields NP and PP chunks with their phrase label.
    """
    for chunk in doc.noun_chunks:
        if chunk.root.head.pos_ == 'ADP':
            span = doc[chunk.start-1:chunk.end]
            yield (span, 'PP')
        yield (chunk, 'NP')


def chunk_tuples_for_doc(doc):
    """
    Generator function that takes a doc and yields ChunkElement tuples.
    """
    for i, (chunk, phrase) in enumerate(chunks_for_doc(doc)):
        yield ChunkElement(cid = 'c' + str(i),
                           head = 't' + str(chunk.root.i),
                           phrase = phrase,
                           text = remove_illegal_chars(chunk.orth_.replace('\n',' ')),
                           targets = ['t' + str(tok.i) for tok in chunk])


def add_chunk_element(chunks_layer, chunk_data, add_comments=False):
    """
    Function that adds a chunk element to the chunks layer.
    """
    chunk_el = etree.SubElement(chunks_layer, "chunk")
    chunk_el.set("id", chunk_data.cid)
    chunk_el.set("head", chunk_data.head)
    chunk_el.set("phrase", chunk_data.phrase)
    span = etree.SubElement(chunk_el, "span")
    if add_comments:
        text = chunk_data.text
        text = prepare_comment_text(text)
        span.append(etree.Comment(text))
    for target in chunk_data.targets:
        target_el = etree.SubElement(span, "target")
        target_el.set("id", target)


def add_dependency_element(dependency_layer, dep_data, add_comments):
    """
    Function that adds dependency elements to the deps layer.
    """
    if add_comments:
        comment = dep_data.rfunc + '(' + dep_data.from_orth + ',' + dep_data.to_orth + ')'
        comment = prepare_comment_text(comment)
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

    while token.head.i != token.i:
        dep_data = DependencyRelation(from_term = 't' + str(token.head.i + 1), # we start counting at 1
                                      to_term = 't' + str(token.i + 1), # we start counting at 1
                                      rfunc = token.dep_,
                                      from_orth = normalize_token_orth(token.head.orth_),
                                      to_orth = normalize_token_orth(token.orth_))
        deps.append(dep_data)
        token = token.head

    return deps


def add_raw_layer(root, raw_layer, cdata=True):
    """
    create raw text layer that aligns with the token layer

    :param lxml.etree._Element root: the root element of the XML file
    :param lxml.etree._Element raw_layer: the 'raw' child of the NAF file

    :rtype: None
    """
    # Add raw layer after adding all other layers + check alignment
    wf_els = root.findall('text/wf')
    tokens = [wf_els[0].text]

    for prev_wf_el, cur_wf_el in zip(wf_els[:-1], wf_els[1:]):
        prev_start = int(prev_wf_el.get('offset'))
        prev_end = prev_start + int(prev_wf_el.get('length'))

        cur_start = int(cur_wf_el.get('offset'))

        delta = cur_start - prev_end  # how many characters are between current token and previous token?

        # no chars between two token (for example with a dot .)
        if delta == 0:
            trailing_chars = ''
        # 1 or more characters between tokens -> n spaces added
        if delta >= 1:
            trailing_chars = ' ' * delta
        elif delta < 0:
            raise AssertionError(f'please check the offsets of {prev_wf_el.text} and {cur_wf_el.text} (delta of {delta})')

        tokens.append(trailing_chars + cur_wf_el.text)

    raw_text = ''.join(tokens)

    if cdata:
        raw_layer.text = etree.CDATA(raw_text)
    else:
        raw_layer.text = raw_text

    # verify alignment between raw and token layer
    for wf_el in root.xpath('text/wf'):
        start = int(wf_el.get('offset'))
        end = start + int(wf_el.get('length'))
        token = raw_layer.text[start:end]
        assert wf_el.text == token, f'mismatch in alignment of wf element {wf_el.text} ({wf_el.get("id")}) with raw layer (expected length {wf_el.get("length")}'

def add_linguisticProcessors_el(naf_header,
                                layer,
                                start_time,
                                end_time,
                                modelname,
                                modelversion=None):
    """

    :return:
    """
    ling_proc = etree.SubElement(naf_header, "linguisticProcessors")
    ling_proc.set("layer", layer)
    lp = etree.SubElement(ling_proc, "lp")
    lp.set("beginTimestamp", start_time)
    lp.set('endTimestamp', end_time)
    lp.set('name', modelname)
    if modelversion:
        lp.set('version', modelversion)


def naf_from_doc(doc,
                 dct,
                 start_time,
                 end_time,
                 modelname,
                 modelversion,
                 naf_version='v3',
                 language='en',
                 comments=False,
                 title=None,
                 uri=None,
                 map_udpos2naf_pos=True,
                 add_mws=True,
                 cdata=True,
                 layer_to_attributes_to_ignore=dict(),
                 layers=['raw',
                         'text',
                         'terms',
                         'entities',
                         'deps',
                         'chunks'],
                 dtd_validation=False):
    """
    Function that takes a document and returns an ElementTree
    object that corresponds to the root of the NAF structure.

    :param bool map_udpos2naf_pos: if True, we use "udpos2nafpos_info"
    to map the Universal Dependencies pos (https://universaldependencies.org/u/pos/)
    to the NAF pos tagset
    """
    # NAF:
    # ---------------------
    # Create NAF tree.
    tree = etree.ElementTree()
    root = etree.Element("NAF")
    tree._setroot(root)
    root.set('{http://www.w3.org/XML/1998/namespace}lang', language)

    root.set('version', naf_version)

    layers = list(layers)

    # Create text and terms layers.
    naf_header = etree.SubElement(root, "nafHeader")

    # add fileDesc child to nafHeader
    filedesc_el = etree.SubElement(naf_header, 'fileDesc')
    filedesc_el.set('creationtime', dct)
    if title is not None:
        filedesc_el.set('title', title)

    # add public child to nafHeader
    public_el = etree.SubElement(naf_header, 'public')
    if uri is not None:
        public_el.set('uri', uri)

    if add_mws:
        layers.append('multiwords')

    for layer in layers:
        add_linguisticProcessors_el(naf_header,
                                    layer,
                                    start_time,
                                    end_time,
                                    modelname,
                                    modelversion)

    if 'raw' in layers:
        raw_layer = etree.SubElement(root, 'raw')
    if 'text' in layers:
        text_layer = etree.SubElement(root, "text")
    if 'terms' in layers:
        terms_layer = etree.SubElement(root, "terms")
    if 'entities' in layers:
        entities_layer = etree.SubElement(root, "entities")
    if 'deps' in layers:
        dependency_layer = etree.SubElement(root, "deps")
    if 'chunks' in layers:
        chunks_layer = etree.SubElement(root, "chunks")

    # Initialize variables:
    # ---------------------
    # - Use a generator for entity awareness.
    entity_gen = entities(doc)
    try:
        next_entity = next(entity_gen)
    except StopIteration:
        next_entity = Entity(start=None, end=None, entity_type=None)

    # - Bookkeeping variables.
    current_term = []    # Use a list for multiword expressions.
    current_term_orth = [] # id.

    current_entity = []    # Use a list for multiword entities.
    current_entity_orth = [] # id.

    current_token = 1    # Keep track of the token number.
    term_number = 1      # Keep track of the term number.
    entity_number = 1    # Keep track of the entity number.

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
                           wordform = token.text,
                           offset = str(token.idx))

            # Create TermElement data:
            spacy_pos = token.pos_
            if map_udpos2naf_pos:
                if spacy_pos in udpos2nafpos_info:
                    pos = udpos2nafpos_info[spacy_pos]['naf_pos']
                    pos_type = udpos2nafpos_info[spacy_pos]['class']
                else:
                    pos = 'O'
                    pos_type = 'open'
            else:
                pos = spacy_pos
                pos_type = 'open'

            term_data = TermElement(id = tid,
                                    lemma = remove_illegal_chars(token.lemma_),
                                    pos = pos,
                                    type=pos_type,
                                    morphofeat = token.tag_,
                                    targets = current_term,
                                    text = current_term_orth)

            if 'text' in layers:
                add_wf_element(text_layer, wf_data, cdata=cdata)
            if 'terms' in layers:
                add_term_element(terms_layer,
                                 term_data,
                                 unwanted_attributes=layer_to_attributes_to_ignore.get('terms', set()),
                                 add_comments=comments)

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
                                            text = current_entity_orth,
                                            ext_refs=[] # entity linking currently not part of spaCy
                                            )
                # Add data to XML:
                if 'entities' in layers:
                    add_entity_element(entities_layer,
                                       naf_version,
                                       entity_data,
                                       add_comments=comments)

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
                    next_entity = Entity(start=None, end=None, entity_type=None)

            # Add dependencies for the current token to the list.
            if 'deps' in layers:
                for dep_data in dependencies_to_add(token):
                    if not dep_data in dependencies_for_sentence:
                        dependencies_for_sentence.append(dep_data)

        # At the end of the sentence, add all the dependencies to the XML structure.
        for dep_data in dependencies_for_sentence:
            if 'deps' in layers:
                add_dependency_element(dependency_layer, dep_data, add_comments=comments)
        current_token = token_number + 1

    if all(['deps' in layers,
            add_mws]):
        add_multi_words(root,
                        naf_version,
                        language)

    # Add chunk layer after adding all other layers.
    for chunk_data in chunk_tuples_for_doc(doc):
        if 'chunks' in layers:
            add_chunk_element(chunks_layer, chunk_data, add_comments=comments)

    # Add raw layer after adding all other layers + check alignment
    add_raw_layer(root, raw_layer, cdata=cdata)

    assert raw_layer.text == doc.text, f'{len(raw_layer.text)} - {len(doc.text)}'


    if dtd_validation:
        dtd = NAF_VERSION_TO_DTD[naf_version]
        validate_naf_file(dtd, root)

    return tree


def time_in_correct_format(datetime_obj):
    "Function that returns the current time (UTC)"
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")


def text_to_NAF(text,
                nlp,
                dct,
                layers,
                title=None,
                uri=None,
                language='en',
                layer_to_attributes_to_ignore=dict(),
                naf_version='v3',
                cdata=True,
                replace_hidden_characters=False,
                map_udpos2naf_pos=False,
                add_mws=True,
                dtd_validation=False):
    """
    Function that takes a text and returns an xml object containing the NAF.
    """
    if replace_hidden_characters:
        text_to_use = text.translate(hidden_table)
    else:
        text_to_use = text

    assert len(text) == len(text_to_use)

    dct_correct_format = time_in_correct_format(dct)

    start_time = time_in_correct_format(datetime.now())
    doc = nlp(text_to_use)

    end_time = time_in_correct_format(datetime.now())

    model_name = f'spaCy-model_{nlp.meta["lang"]}_{nlp.meta["name"]}'
    model_version = f'spaCy_version-{spacy.__version__}__model_version-{nlp.meta["version"]}'
    return naf_from_doc(doc=doc,
                        dct=dct_correct_format,
                        start_time=start_time,
                        end_time=end_time,
                        modelname=model_name,
                        modelversion=model_version,
                        naf_version=naf_version,
                        language=language,
                        title=title,
                        uri=uri,
                        layers=layers,
                        add_mws=add_mws,
                        cdata=cdata,
                        layer_to_attributes_to_ignore=layer_to_attributes_to_ignore,
                        map_udpos2naf_pos=map_udpos2naf_pos,
                        dtd_validation=dtd_validation)

def NAF_to_string(NAF, byte=False):
    """
    Function that takes an XML object containing NAF, and returns it as a string.
    If byte is True, then the output is a bytestring.
    """
    xml_string = etree.tostring(NAF, pretty_print=True, xml_declaration=True, encoding='utf-8')
    if byte:
        return xml_string
    else:
        return xml_string.decode('utf-8')

def NAF_to_file(NAF, output_path):
    NAF.write(output_path,
              encoding='utf-8',
              pretty_print=True,
              xml_declaration=True)

# Command line functionality: given name of a file, process the file contents and
# print the NAF to stdout.
if __name__ == '__main__':
    import sys
    import spacy
    from datetime import datetime

    nlp = spacy.load('en_core_web_sm')

    layer_to_attributes_to_ignore = {
        'terms' : {'morphofeat', 'type'} # this will not add these attributes to the term element
    }
    with open(sys.argv[1]) as f:
        text = f.read()
        naf = text_to_NAF(text,
                         nlp,
                         dct=datetime.now(),
                         layers={'raw',
                                 'text',
                                 'terms',
                                 'deps'},
                          replace_hidden_characters=False,
                          naf_version='v3.1',
                          add_mws=True,
                          layer_to_attributes_to_ignore=layer_to_attributes_to_ignore,
                          dtd_validation=False)

        print(NAF_to_string(naf))
        #NAF_to_file(naf, 'example_files/output.xml')
