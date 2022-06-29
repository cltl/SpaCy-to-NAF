import os.path

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
    naf = s2n.convert(text, out_path)
    assert len(naf.get('text')) == len(naf.get('terms')) == len(set([wf.id for wf in naf.get('text')])) > 0
    assert naf.get('entities')
    assert naf.get('chunks')
    assert naf.get('deps')
