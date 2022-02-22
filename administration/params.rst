========================
Configuration parameters
========================

Introduction
============
As you already know The OdooPBX Asterisk connection middleware is based on the Saltstack pltaform.

* Odoo connects to the salt-api.
* The salt-api forwards requests to the salt-master.
* The salt-master sends requests to the Asterisk.

All configuration is located in ``/etc/salt`` folder.

Below we review the options we use in order to configure it all.

The minion
==========
The main minion's configuration file is ``/etc/salt/minion``.

The defaults are located in ``/etc/salt/minion.d/odoopbx.conf``.

Instead of changing the defaults just add a required option to ``/etc/salt/minion_local.conf``.

You must restat the minion process after making changes to its configuration using.

Below is the list of default parameters and their meanings.

.. autoyaml:: /agent/salt/agent/files/etc/minion.d/odoopbx.conf

