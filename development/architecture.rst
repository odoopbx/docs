====================
OdooPBX architecture
====================

Introduction
============

As it comes from its name OdooPBX is a PBX platform built upon Odoo & Asterisk.


Let's dive into the details now.

The Agent
=========


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







