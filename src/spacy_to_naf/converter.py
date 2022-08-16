import argparse
import os.path
from pathlib import Path
from typing import Union

import spacy
from nafparserpy.layers.chunks import Chunk
from nafparserpy.layers.deps import Dep
from nafparserpy.layers.elements import Span
from nafparserpy.layers.entities import Entity
from nafparserpy.layers.naf_header import LPDependency
from nafparserpy.layers.terms import Term
from nafparserpy.layers.text import Wf
from nafparserpy.parser import NafParser


def map_pos(map_udpos2naf_pos: bool, token):
    spacy_pos = token.pos_
    if map_udpos2naf_pos:
        if spacy_pos in ud2naf_pos:
            pos = ud2naf_pos[spacy_pos]['naf_pos']
            pos_type = ud2naf_pos[spacy_pos]['class']
        else:
            pos = 'O'
            pos_type = 'open'
    else:
        pos = spacy_pos
        pos_type = 'open'
    return pos, pos_type


ud2naf_pos = {
    'ADJ': {
        'class': 'open',
        'naf_pos': 'G'
    },
    'ADP': {
        'class': 'open',
        'naf_pos': 'P'
    },
    'ADV': {
        'class': 'open',
        'naf_pos': 'A'
    },
    'AUX': {
        'class': 'close',
        'naf_pos': 'V',
    },
    'CCONJ': {
        'class': 'close',
        'naf_pos': 'C'
    },
    'DET': {
        'class': 'close',
        'naf_pos': 'D'
    },
    'INTJ': {
        'class': 'open',
        'naf_pos': 'O'
    },
    'NOUN': {
        'class': 'open',
        'naf_pos': 'N'
    },
    'NUM': {
        'class': 'close',
        'naf_pos': 'O'
    },
    'PART': {
        'class': 'close',
        'naf_pos': 'O'
    },
    'PRON': {
        'class': 'close',
        'naf_pos': 'O'
    },
    'PROPN': {
        'class': 'open',
        'naf_pos': 'R'
    },
    'PUNCT': {
        'class': 'close',
        'naf_pos': 'O'
    },
    'SCONJ': {
        'class': 'close',
        'naf_pos': 'O'
    },
    'SYM': {
        'class': 'open',
        'naf_pos': 'O'
    },
    'VERB': {
        'class': 'open',
        'naf_pos': 'V'
    },
    'X': {
        'class': 'open',
        'naf_pos': 'O'
    },
    'SPACE': {
        'class': 'open',
        'naf_pos': 'O'
    }
}


def without_extension(filename: str) -> str:
    return ".".join(filename.split('.')[:-1])


START_INDEX = 1
"""start index (0/1) for NAF element ids"""


def extract_text(doc):
    wfs = []
    for sent_i, sentence in enumerate(doc.sents):
        for token in sentence:
            wf = Wf(token.text, wf_id(token.i), str(token.idx), str(len(token.text)), sent=sent_id(sent_i))
            wfs.append(wf)
    return wfs


def extract_terms(doc, map_ud2nafpos: bool = False):
    terms = []
    for sent_i, sentence in enumerate(doc.sents):
        for token in sentence:
            pos, pos_type = map_pos(map_ud2nafpos, token)
            term = Term(term_id(token.i),
                        Span.create([wf_id(token.i)]),
                        lemma=token.lemma_,
                        pos=pos,
                        type=pos_type,
                        morphofeat=token.tag_)
            terms.append(term)
    return terms


def extract_deps(doc):
    deps = []
    for token in doc:
        if token.i == token.head.i:
            continue
        deps.append(Dep(term_id(token.head.i), term_id(token.i), token.dep_))
    return deps


def sent_id(i):
    return str(i + START_INDEX)


def element_id(pfx, i):
    return f"{pfx}{i + START_INDEX}"


def entity_id(i):
    return element_id("e", i)


def term_id(i):
    return element_id("t", i)


def wf_id(i):
    return element_id("w", i)


def chunk_id(i):
    return element_id("ch", i)


def extract_entities(doc):
    return [Entity.create(entity_id(i),
                          ent.label_,
                          [term_id(x) for x in range(ent.start, ent.end)])
            for i, ent in enumerate(doc.ents)]


def extract_chunks(doc):
    return [Chunk(chunk_id(i),
                  term_id(chunk.root.i),
                  chunk.label_,
                  Span.create([term_id(x) for x in range(chunk.start, chunk.end)]))
            for i, chunk in enumerate(doc.noun_chunks)]


class Converter:
    def __init__(self,
                 spacy_model: str = 'en_core_web_sm',
                 add_terms=False,
                 add_deps=False,
                 add_entities=False,
                 add_chunks=False,
                 map_udpos=False):
        self.processor_name = 'spacy_to_naf'
        self.processor_version = '0.2.0'
        self.nlp = spacy.load(spacy_model)
        self.model_name = f'spaCy-model_{self.nlp.meta["lang"]}_{self.nlp.meta["name"]}'
        self.model_version = f'spaCy_version-{spacy.__version__}__model_version-{self.nlp.meta["version"]}'
        self.add_terms = add_terms
        self.add_entities = add_entities
        self.add_chunks = add_chunks
        self.add_deps = add_deps
        self.map_udpos = map_udpos

    def convert(self, text: str, naf: NafParser, out_path: Union[str, None] = None):
        doc = self.nlp(text)
        self.add_text_layer(doc, naf)
        if self.add_terms:
            self.add_terms_layer(doc, naf)
        if self.add_deps:
            self.add_deps_layer(doc, naf)
        if self.add_entities:
            self.add_entities_layer(doc, naf)
        if self.add_chunks:
            self.add_chunks_layer(doc, naf)
        if out_path is not None:
            naf.write(out_path)
        return naf

    def init_naf(self, filename, text):
        naf = NafParser(filename=filename, decorate=False)
        naf.add_raw_layer(text)
        naf.add_linguistic_processor('raw', self.processor_name, self.processor_version)
        return naf

    def add_text_layer(self, doc, naf):
        naf.add_layer_from_elements('text', extract_text(doc), exist_ok=True)
        self.add_linguistic_processor('text', naf)

    def add_terms_layer(self, doc, naf):
        naf.add_layer_from_elements('terms', extract_terms(doc, self.map_udpos), exist_ok=True)
        self.add_linguistic_processor('terms', naf)

    def add_linguistic_processor(self, layer: str, naf: NafParser):
        naf.add_linguistic_processor(layer, self.processor_name, self.processor_version,
                                     lpDependencies=[LPDependency(self.model_name, self.model_version)])

    def add_entities_layer(self, doc, naf: NafParser):
        if doc.ents:
            naf.add_layer_from_elements('entities', extract_entities(doc), exist_ok=True)
            self.add_linguistic_processor('entities', naf)

    def add_chunks_layer(self, doc, naf):
        if doc.noun_chunks:
            naf.add_layer_from_elements('chunks', extract_chunks(doc), exist_ok=True)
            self.add_linguistic_processor('chunks', naf)

    def add_deps_layer(self, doc, naf):
        naf.add_layer_from_elements('deps', extract_deps(doc), exist_ok=True)
        self.add_linguistic_processor('deps', naf)

    def process_naf(self, naf: NafParser, out_path: Union[str, None] = None):
        return self.convert(naf.get('raw').text, naf, out_path)

    def convert_naf_files(self, input_path, output_dir):
        for path in Path(input_path).rglob('*.naf'):
            naf = NafParser.load(str(path), decorate=False)
            filename = os.path.basename(path)
            self.process_naf(naf, os.path.join(output_dir, filename))

    def process_text(self, text: str, filename: str, out_path: Union[str, None] = None):
        naf = self.init_naf(filename, text)
        return self.convert(text, naf, out_path)

    def convert_text_files(self, input_path, output_dir):
        for path in Path(input_path).rglob('*.txt'):
            with open(path) as f:
                text = f.read()
            filename = f'{without_extension(os.path.basename(path))}.naf'
            self.process_text(text, filename, os.path.join(output_dir, filename))

    def run(self, input_path, filename=None, output_dir=None, is_naf_input=False):
        if os.path.exists(input_path):
            if output_dir is not None and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if is_naf_input:
                self.convert_naf_files(input_path, output_dir)
            else:
                self.convert_text_files(input_path, output_dir)
        else:
            self.convert(input_path, filename, output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spacy-to-Naf converter. Inputs text or text files and outputs'
                                                 'Naf files with tokenized text. POS-tagged terms, dependencies, '
                                                 ' entities and chunks can be included using the '
                                                 'corresponding flag.')
    parser.add_argument('-i', '--input', type=str, help='input path or text')
    parser.add_argument('-f', '--filename', type=str, help='filename. Inferred from input if input is a path')
    parser.add_argument('-o', '--output_dir', type=str, help='output dir path. File will only be written if set.')
    parser.add_argument('-n', '--is_naf_input', action='store_true', help='input is NAF formatted')
    parser.add_argument('-m', '--spacy_model', type=str, help='name of spacy model. The model should be have been '
                                                              'downloaded.')
    parser.add_argument('-t', '--terms', action='store_true', help='extract POS tagged terms')
    parser.add_argument('-d', '--deps', action='store_true', help='extract dependencies')
    parser.add_argument('-e', '--entities', action='store_true', help='extract entities')
    parser.add_argument('-c', '--chunks', action='store_true', help='extract noun chunks')
    parser.add_argument('-u', '--ud_pos', action='store_true', help='map POS tags to universal-dependencies tagset')
    args = parser.parse_args()

    converter = Converter(args.spacy_model, args.terms, args.deps, args.entities, args.chunks, args.ud_pos)
    converter.run(args.input, args.filename, args.output, args.is_naf_input)
