`spacy-to-naf` is a [spaCy](https://spacy.io/) wrapper that converts text or 
[NAF](https://github.com/cltl/NAF-4-Development) input to NAF.
The converter minimally extracts a tokenized `text` layer, and can additionally extract `terms`, `deps`, `entities` and 
`chunks` layers.

## Installation
To install `spacy-to-naf`:
```
pip install spacy-to-naf
```
Download a spaCy model, eg. 'en-core-web-sm':
```
python -m spacy download en-core-web-sm
```

## Usage
Specify the spaCy model and the NAF layers to create (the `text` layer is always created).
```python
from spacy_to_naf.converter import Converter
converter = Converter('en-core-web-sm', add_terms=True, add_deps=True, add_entities=True, add_chunks=True)
```
The input may be a naf or text directory or a text string. 

### Text input
To convert text to a file 'example.naf' in the current directory:
```python
text = """The cat sat on the mat. Felix was his name."""
naf = converter.convert(text, 'example.naf', '.')
```
The converter additionally returns a [NafParser](https://cltl.github.io/nafparserpy/) object for further
processing.

### Processing files
To process text files from a 'text_in' to 'naf_out' directory:
```python
converter.convert_files('text_in', 'naf_out')
```
*Note that input text files are expected to end in '.txt'.*

To process NAF files from 'naf_in' to 'naf_out':
```python
converter.convert_naf_files('naf_in', 'naf_out')
```
Output files carry the same name as the input file, extension excepted.
