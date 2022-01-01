====================
OdooPBX architecture
====================

Introduction
============

As it comes from its name OdooPBX is a PBX platform built upon Odoo & Asterisk.

Odoo (former OpenERP / TinyERP) is a modern WEB business platform that rapidly spreads over the world.

.. note::

  Odoo as a WEB development platform has the following features:

  * A modern architecture with clean separation of layers (MVC).
    UI is created in XML, business logic is programmed in Python, data is stored in PostgreSQL and accessed
    through ORM (object-relational mapper).
  * Rapid application development - Odoo is a blazing fast development tool that allows building new
    apps like a lightning.
  * Granular security system with row-level colum-level access.
  * Safe upgrade framework give a possibility of reliable upgrades.


Odoo as a business platform comes with a plenty of ready to use business oriented modules like CRM, Projects, Warehouse, 
Sales, Events, etc.

So from one side OdooPBX is a PBX management tool built upon Odoo WEB framework.

From another side OdooPBX adds a telephony layer to existing business modules and by this
integrating tight phone communications with places they happen.

Finally a special middleware Agent is used to connect Odoo and Asterisk together in a proper way.

Let's dive into the details now.

The Agent
=========
The Agent itself is built upon the Saltstack platform and performs the following functions:

* Forwards Asterisk events to Odoo according to the downloaded events map.
* Executes Asterisk actions received from Odoo.
* Protects Asterisk from DDoS and password bruteforce attacks.
* Manages the installation & upgrade process.

Engines
#######
`Salt Engines <https://docs.saltproject.io/en/latest/topics/engines/index.html>`__ 
are long-running, external system processes that leverage Salt. 

The Agent has the following engines:

* AMI engine (asterisk_ami);
* Asterisk WEB console engine (asterisk_cli);
* Odoo bus connector engine (odoo_connector);


AMI engine
++++++++++
AMI (Asterisk Manager Interface) engine connects to the Asterisk AMI port (usually 5038) and 
forwards AMI events to Odoo according to the events map that is downloaded on the Agent startup.

Events map is defined in the Asterisk Common module. Each event has the following structure:

* **name** - AMI event name. Examples: ``Hangup``, ``CDR``, ``OriginateResponse``.
* **source** - ``AMI`` for now.
* **model** - Odoo app and model that will receive the event. Example: ``asterisk_common.user``.
* **method** - model's method that will be called. Example: ``ami_originate_response``.
* **condition** - an optional condition evaluated on the Agent side on the event's data. 
  Example: ``event['Response'] == 'Failure'`` (only failure response will be send to Odoo).
* **delay** - an optional delay in seconds before sending the event to Odoo. Sometimes it is required to
  let previous event to be processed by Odoo. Example: ``1.5``.

Modules
#######

States
######

OdooPBX modules
===============

Asterisk Base
#############

Asterisk Calls
##############







