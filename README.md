# Odoo PBX documentation
The OdooPBX documentation is published here - https://odoopbx.github.io/docs.

In order to develop OdooPBX documentation you must roll out the developer environment.

The documentation is built on Sphinx. It uses autodoc module to generate API from the source code so Odoo & Asterisk Plus addons must be installed. 

Below is a short instruction how to prepare the environment on Ubuntu 20.04.

## System libs installation
Install deps for Odoo 15.0 libs:
```
apt update
apt install -y git python3-pip build-essential wget python3-dev python3-venv \
    python3-wheel libfreetype6-dev libxml2-dev libzip-dev libldap2-dev libsasl2-dev \
    python3-setuptools node-less libjpeg-dev zlib1g-dev libpq-dev \
    libxslt1-dev libldap2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
    liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev
```

## Odoo 15.0 libs installation
```
cd /opt/
wget https://github.com/odoo/odoo/archive/refs/heads/15.0.zip
unzip 15.0.zip
python3 -m pip install --upgrade pip
python3 -m pip install wheel
python3 -m pip install odoo-15.0
python3 -m pip install -r odoo-15.0/requirements.txt
rm -rf 15.0 odoo-15.0
```
## Clone the docs repo
```
python3 -m pip install sphinx sphinx-serve sphinx_nameko_theme
cd /srv
git clone git@github.com:odoopbx/docs.git
cd docs
mkdir _build
cd _build/
ln -s ../docs/ html
cd .. 
python3 -m sphinx  -t html . docs/
```
In order to preview your docs use Sphinx serve:
```
python3 -m sphinx_serve
```
