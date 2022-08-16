## 0.2.0 - 2022-08-16
### Changed
- naf conversion builds on existing naf tree instead of creating a new one

## 0.1.0 - 2022-07-19
### Changed
- replaced conversion script with module; Converter class used to preload spacy model for file processing
- converter accepts text string or input directory of either naf or text files as input
- input texts are kept as is, without replacement of whitespace characters
- only the latest naf version is supported

### Removed
- particle-verb pairs and multiwords are not identified anymore

## 27-1-2020
- added keyword argument **naf_version** to be able to differentiate between NAF version 3 and 4

## 23-1-2020

- added keyword argument **layer_to_attributes_to_ignore** to indicate
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
