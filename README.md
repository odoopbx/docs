# OdooPBX Documentation
This repository contains the sources for the OdooPBX documentation available here: https://docs.odoopbx.com.

It is powered by [Sphinx documentation](https://docs.odoopbx.com) and
uses autodoc module to generate parts of the documentation from the source code of [addons](https://github.com/odoopbx/addons) and [pbx](https://github.com/odoopbx/pbx) repositories.

It means that in order to successfully build OdooPBX documentation you will have to setup a developer environment.


## Docker Development Environment
Prepair the environment:
```
docker pull odoopbx/odoo:15.0
git clone https://github.com/odoopbx/docs.git
git clone https://github.com/odoopbx/addons.git
git clone https://github.com/odoopbx/pbx.git
docker run -d -u 0 -p 8081:8081/tcp \
  -v $PWD/docs:/srv/docs \
  -v $PWD/addons:/srv/addons \
  -v $PWD/pbx:/srv/pbx \
  --name docs odoopbx/odoo:15.0 sleep 100d
```

Now you have a container named `docs` ready to build the docs.
Install the requirements as `root`:
```
docker exec -u 0 docs pip3 install -r /srv/docs/requirements.txt
```

The `docs` container is preapared to build the docs.
To eliminate file permision issues we build documentation with the UID of current user:
```
docker exec -u $UID -it docs bash
cd /srv/docs
./build.sh
```


## Ubuntu 20.04 Development Environment
Below is an instruction on how to prepare the environment under Ubuntu 20.04.

### System libs installation
Install deps for Odoo 15.0 libs:
```
apt update
apt install -y git python3-pip build-essential wget python3-dev python3-venv \
    python3-wheel libfreetype6-dev libxml2-dev libzip-dev libldap2-dev libsasl2-dev \
    python3-setuptools node-less libjpeg-dev zlib1g-dev libpq-dev \
    libxslt1-dev libldap2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
    liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev
```

### Odoo 15.0 installation
```
cd /srv/
wget https://github.com/odoo/odoo/archive/refs/heads/15.0.zip
unzip 15.0.zip
python3 -m pip install --upgrade pip
python3 -m pip install wheel
python3 -m pip install odoo-15.0/
python3 -m pip install -r odoo-15.0/requirements.txt
rm -rf 15.0 odoo-15.0
```
### Clone our repos
```
cd /srv
git clone https://github.com/odoopbx/docs.git
git clone https://github.com/odoopbx/addons.git
git clone https://github.com/odoopbx/pbx.git
python3 -m pip install -r docs/requirements.txt
python3 -m pip install -r addons/requirements.txt
cd docs
./build.sh
```

## Change, Build, Repeat
`build.sh` is a tiny script which utilizes sphinx module to create HTML files inside `_build/` subdirectory. After successfull build it prints out finally:
```
The HTML pages are in srv/docs/_build.
```

We reapeat `./build.sh` after making changes to re-generate HTML files.

You can point your browser to `_build/` directory inside `docs` repository.

Or run a simple web-server with `sphinx-serve` command from `/srv/docs` directory.
It listens on port `8081` by default as seen from it's output logs:

```
I have no name!@f2559b118194:/srv/docs$ sphinx-serve 
:: Found documentation at: /srv/docs/_build/html
:: Serving documentation at http://0.0.0.0:8081
:: Terminate with Ctrl-C
```
