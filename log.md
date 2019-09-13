
## 13-9-2019
- added SPACE to mapping spacy_to_naf.udpos2nafpos_info
- default value 'O' if pos value not found

## 12-9-2019
- token and terms now start at one
- created mapping in spacy_to_naf.udpos2nafpos_info to map [UD pos](https://universaldependencies.org/u/pos/) to [NAF pos](https://github.com/newsreader/NAF)
    - NUM is problematic in the mapping -> now mapped to 'O'
- added 'type' attribute to term layer: open or closed
