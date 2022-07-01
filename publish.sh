#!/bin/bash

set -e

git checkout public
git pull
rm -rf docs
cp -r _build docs
[ -e docs/html ] && rm docs/html
touch docs/.nojekyll
echo "docs.odoopbx.com" > docs/CNAME
git add docs
git commit docs -m "Docs updated"
git push
git checkout master
git push

