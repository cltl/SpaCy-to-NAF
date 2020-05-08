#!/usr/bin/env bash

rm -r output
mkdir output

python v4_validation.py > output/v4_validation.naf 2> output/v4_validation.err
python v4_raw_text_terms.py > output/v4_raw_text_terms.naf 2> output/v4_raw_text_terms.err
python v4_add_entity.py > output/v4_add_entity.naf 2> output/v4_add_entity.err
python v4_raw_text_terms_deps.py > output/v4_raw_text_terms_deps.out 2> output/v4_raw_text_terms_deps.err
