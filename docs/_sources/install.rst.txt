============
Installation
============
OdooPBX installation is managed by the Saltstack configuration management tool
and includes formulas for installing all needed components:

* PostgreSQL database for Odoo;
* Odoo with the ``Asterisk Plus`` modules;
* Asterisk IP-PBX;
* Agent;
* Nginx frontend;
* Letsencrypt based PKI management.
  
Probably you already have some of components already running in your environment.
In this case you need to install the missing parts.

.. toctree::
   :titlesonly:

   install/demo
   install/system
   install/standard
   install/docker
   install/freepbx

