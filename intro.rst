============
Introduction
============

What is OdooPBX?
================
OdooPBX is a PBX platform built upon Odoo & Asterisk using Saltstack API as a middleware layer.

* `Odoo <https://odoo.com>`_ (former OpenERP / TinyERP) is a modern WEB business platform that rapidly spreads over the world.
* `Asterisk PBX <https://asterisk.org>`_ is the most popular world open source PBX software.
* `Saltstack <https://docs.saltproject.io/en/latest/>`__ is automation, infrastructure management, remote execution, 
  configuration management, data-driven orchestration, and so much more.

.. note::

  Odoo as a WEB development platform has the following features:

  * A modern architecture with clean separation of layers.
    UI is created in XML, business logic is programmed in Python, data is stored in PostgreSQL and accessed
    through an ORM (object-relational mapper).
  * Rapid application development - Odoo is a blazing fast development tool that allows building new
    apps like a lightning.
  * Granular security system with row-level colum-level access.
  * Safe upgrade framework give a possibility of reliable upgrades.


Odoo as a business platform comes with a plenty of ready to use business oriented modules like CRM, Projects, Warehouse, 
Sales, Events, etc.

So from one side OdooPBX is a PBX management tool built upon Odoo WEB framework.

From another side OdooPBX adds a telephony layer to existing business modules and by this
integrating tight phone communications with places they happen.

.. note:: 

    With OdooPBX you create phone applications writing 100% Odoo code.

Finally a special middleware Agent is used to connect Odoo and Asterisk together in a proper way.

**The Agent itself is built upon the Saltstack** platform and performs the following functions:

* Forwards Asterisk events to Odoo according to the downloaded events map.
* Executes Asterisk actions received from Odoo.
* Protects Asterisk from DDoS and password bruteforce attacks.
* Manages the installation & upgrade process.

OdooPBX is **extremely adaptable and extensible** because Odoo is very adaptable
by its prominent `inheritance architecture <https://www.odoo.com/documentation/14.0/developer/howtos/rdtraining/13_inheritance.html>`__
and Salt is extensible because it is built to be that.

The Saltstack platform has tons of ready to use building blocks called `execution modules <https://docs.saltproject.io/en/latest/ref/modules/all/index.html>`__
that can be used to extend Odoo's communications with external world and make it
extremely quicky to create and maintain.

Read the `Developers guide <../development>`_ for more information on how to build telephony applications on the OdooPBX platform.

Back to the `contents <../>`_.
