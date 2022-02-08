#!/bin/bash

rm -rf _build
python3.7 -m sphinx -t html . _build
cd _build
# Create a link for sphinx-serve
ln -s . html
