#!/usr/bin/env bash

rm -rf dep
mkdir dep
cd dep

git clone https://github.com/cltl/NAF-4-Development
cp NAF-4-Development/res/naf_development/naf_v4.dtd ../example_files