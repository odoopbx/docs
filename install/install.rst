============
Installation
============

.. toctree::

OdooPBX installation is managed by the Saltstack configuration management software and includes formulas for installing all needed components:

* PostgreSQL database for Odoo.
* Odoo with the ``Asterisk Plus`` module.
* Asterisk IP-PBX.
* Agent.
* Nginx frontend.
* Letsencrypt based PKI management.
  
Probably you already have some of components already running in your environment.
Then choose from menu below for instuctions to install the missing parts.

If you need to setup everything from scratch check our :doc:`quickstart` guide.


.. toctree::
    :titlesonly:

    quickstart
    system
    standard
    docker    
    demo