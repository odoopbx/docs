#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

rm -rf $DIR/_build
python3.10 -m sphinx -t html $DIR $DIR/_build
cd $DIR/_build
# Create a link for sphinx-serve
ln -s . $DIR/_build/html
