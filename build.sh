#!/bin/bash

set -e

rm -rf _build
python3 -m sphinx -t html . _build
cd _build
# Create a link for sphinx-serve
ln -s . html
