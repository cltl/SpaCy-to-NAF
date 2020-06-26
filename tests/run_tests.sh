#!/usr/bin/env bash

rm -r output
mkdir output

#python v31_validation.py > output/v31_validation.naf 2> output/v31_validation.err
python v31_raw_text_terms.py > output/v31_raw_text_terms.naf 2> output/v31_raw_text_terms.err
#python v31_add_entity.py > output/v31_add_entity.naf 2> output/v31_add_entity.err
python v31_raw_text_terms_deps.py > output/v31_raw_text_terms_deps.naf 2> output/v31_raw_text_terms_deps.err
python v31_raw_text_terms_deps_mw.py > output/v31_raw_text_terms_deps_mw.naf 2> output/v31_raw_text_terms_deps_mw.err
#python v31_it_raw_text_terms.py
#python v31_raw_text_no_cdata.py > output/v31_raw_text_no_cdata.naf 2> output/v31_raw_text_no_cdata.err
