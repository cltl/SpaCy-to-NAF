## 23-1-2020

-added keyword argument **layer_to_attributes_to_ignore** to indicate
which attributes you want to exclude. Now only implemented for terms.

## 25-9-2019
-added function **NAF_to_file** which  uses etree.ElementTree.write to write NAF to file.

## 20-9-2019
- added keyword **replace_hidden_characters** to **text_to_NAF** which allows to replace hidden characters to ' '
- fixed the 'deps' layer, which was stuck in a while loop.

## 15-9-2019
- added 'resource' to EntityElement. In next version, we can create a namedtuple for external references.

## 13-9-2019
- added SPACE to mapping spacy_to_naf.udpos2nafpos_info
- default value 'O' if pos value not found

## 12-9-2019
- token and terms now start at one
- created mapping in spacy_to_naf.udpos2nafpos_info to map [UD pos](https://universaldependencies.org/u/pos/) to [NAF pos](https://github.com/newsreader/NAF)
    - NUM is problematic in the mapping -> now mapped to 'O'
- added 'type' attribute to term layer: open or closed
