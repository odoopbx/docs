# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_nameko_theme
import os,sys
DIR = os.path.dirname(__file__)
sys.path.insert(
    0, os.path.abspath(
        os.path.join(DIR, '_extensions')))
sys.path.append('/srv/odoo/14.0/src')
import odoo
odoo.addons.__path__.append('/srv/odoopbx/addons')
odoo.addons.__path__.append('/srv/odoo/14.0/addons')
odoo.addons.__path__.append('/srv/odoo/14.0/src/addons')
import odoo.addons


project = 'OdooPBX'
copyright = '2022, Odooist'
author = 'Odooist'
release = '1.0'

extensions_path = '_extensions'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.ifconfig',
    'sphinx.ext.todo',
    'embedded_video',
    'html_domain',
    'redirects',    
    'sphinx.ext.napoleon',

]

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'sphinx-env', 'docs']

html_theme = 'nameko'
html_theme_path = [sphinx_nameko_theme.get_html_theme_path()]
html_static_path = ['_static']
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"
html_show_sphinx = False
html_show_sourcelink = False
