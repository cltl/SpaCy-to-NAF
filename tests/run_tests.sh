#!/usr/bin/env bash

rm -r output
mkdir output

python v4_raw_text_terms.py > output/v4_raw_text_terms.naf 2> output/v4_raw_text_terms.err
#python add_entity.py
#python add_dependency.py
