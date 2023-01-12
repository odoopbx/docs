.. contents::

What is OdooPBX?
================
OdooPBX is a telephony platform built upon Odoo & Asterisk using Nameko microservices as a middleware layer:

* `Odoo <https://odoo.com>`_ (former OpenERP / TinyERP) is a modern WEB business platform that rapidly spreads over the world.
* `Asterisk PBX <https://asterisk.org>`_ is the most popular open source PBX software.
* `Nameko <https://www.nameko.io/>`__ is a microservice framework for Python, that is focused on business logic, distributed, scalable and extensible.

Odoo as a business platform comes with a plenty of ready to use business oriented modules like CRM, Projects, Warehouse, 
Sales, Events, Website and much more.

OdooPBX adds a layer of telephony to these business modules and thus integrates close telephone communication with the places where it takes place.

Finally, a special middleware **Agent** is used to connect Odoo and Asterisk together in a proper way.

The Agent itself is built upon the Nameko framework and performs the following functions:

* Forwards Asterisk AMI events to Odoo according to the downloaded events map.
* Executes Asterisk AMI actions received from Odoo.
* Protects Asterisk from DDoS and password bruteforce attacks.
* Provides a backend part for a WEB based Asterisk CLI.

Read the `Developers guide <../development>`_ for more information on how to build telephony applications on the OdooPBX platform.

OdooPBX Apps
============
As OdooPBX is based on Odoo it has modular architecture.

.. note::

  The list of modules can be found in `addons repo <https://github.com/odoopbx/addons>`_


The main module is named **Asterisk Plus** and it is inherited by all other OdooPBX modules. 

Other modules add some integration between Asterisk Plus module and different Odoo componoents. For example, Asterisk Plus CRM app requires CRM module to be installed
and brings the integration of CRM and telephony.

Installation types
==================
Depending on your existing environment there can be different installation types. 

* If you have Odoo & Asterisk already running you need to install the OdooPBX agent and configure it for your Odoo and Asterisk instances.
* If you have only Odoo running then you need to also install Asterisk and the Agent.
* If you have Asterisk running then you should install the Agent on the Asterisk server and also install an Odoo instance near it.
* Finally, you might start from zero and would want to install everything from scratch. 

The OdooPBX software is distributed using Docker Compose style.

All these topics are covered in the :doc:`install` section.
