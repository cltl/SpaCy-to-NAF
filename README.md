# spaCy to NAF

This repository contains everything you need to output SpaCy results in NAF format.

Please check **log.md** for updates on the conversion script.

**Example**:

```python
import spacy_to_naf
import spacy

nlp = spacy.load('en')

text = """The cat sat on the mat. Felix was his name."""

NAF = spacy_to_naf.text_to_NAF(text, nlp)
print(spacy_to_naf.NAF_to_string(NAF))
```

Or use the command line:
```
python spacy_to_naf.py example_files/felix.txt > example_files/felix.naf
```

NB. Don't use this for batch processing! That would mean loading SpaCy for each
file, which is wildly inefficient. For large batches, write a python script that
loads SpaCy and this module, loops over the files, and writes out NAF in one go.

## TODO
* add https://github.com/huggingface/neuralcoref

