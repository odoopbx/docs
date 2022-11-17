==============================
Agent Configuration parameters
==============================

Introduction
============
As you already know The OdooPBX Asterisk connection middleware is based on the Saltstack pltaform.

* Odoo connects to the salt-api.
* The salt-api forwards requests to the salt-master.
* The salt-master sends requests to the connected salt-minion.
* The salt-minion is connected to the Asterisk via AMI port.

All configuration is located in ``/etc/salt`` folder.

Below we review the options we use in order to configure it all.

Minion configuration
====================
The main minion's configuration file is ``/etc/salt/minion``.

The defaults are located in ``/etc/salt/minion.d/odoopbx.conf``.

Instead of changing the defaults just add a required option to ``/etc/salt/odoopbx/minion.conf``.

You must restat the minion process after making changes to its configuration using.

Below is the list of default parameters and their meanings.

.. autoyaml:: /pbx/salt/agent/files/etc/minion.d/odoopbx.conf

Master and API configuration
============================
Master and API configuration is defined in ``/etc/salt/master``.

It's better to create ``*.conf`` files inside ``/etc/salt/master.d/`` directory
in case you want to modify Salt Master settings.
It will keep your settings when you upgrade the agent.

.. autoyaml:: /pbx/salt/agent/files/etc/master
