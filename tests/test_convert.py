from src.spacy_to_naf.converter import Converter
import os.path


def test_convert():
    converter = Converter('en_core_web_sm', add_terms=True, add_deps=True, add_entities=True, add_chunks=True)

    text = "Hello World"
    naf = converter.run(text, 'hello.naf', 'data')
    assert os.path.exists("data/hello.naf")
