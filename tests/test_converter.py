import os.path

from nafparserpy.parser import NafParser

from src.spacy_to_naf.converter import Converter


def test_converter():
    s2n = Converter(add_terms=True, add_entities=True, add_chunks=True, add_deps=True)
    test_file = 'tests/data/example.txt'
    with open(test_file) as f:
        text = f.read()
    outdir = 'tests/out'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    out_path = os.path.join(outdir, 'example.naf')
    naf = s2n.process_text(text, 'example.naf', out_path)
    assert len(naf.get('text')) == len(naf.get('terms')) == len(set([wf.id for wf in naf.get('text')])) > 0
    assert naf.get('entities')
    assert naf.get('chunks')
    assert naf.get('deps')


def test_naf_conversion():
    s2n = Converter(add_terms=True, add_entities=True, add_chunks=True, add_deps=True)
    test_file = 'tests/data/example.txt'
    with open(test_file) as f:
        text = f.read()
    outdir = 'tests/out'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    out_path = os.path.join(outdir, 'example.naf')
    naf = NafParser(filename='example.naf')
    naf.add_raw_layer(text)
    naf.add_linguistic_processor('raw', 'test', '0.1')
    naf = s2n.process_naf(naf, out_path)
    assert len(naf.get('text')) == len(naf.get('terms')) == len(set([wf.id for wf in naf.get('text')])) > 0
    assert naf.get('entities')
    assert naf.get('chunks')
    assert naf.get('deps')