==============================
Agent Parameters
==============================
OdooPBX Agent consists of three services:

 * salt-api: provides the salt API at TCP port ``48000`` by default.
 * salt-master: Pub/Sub message bus based on ZeroMQ. more on [Salt architecture](https://docs.saltproject.io/en/latest/topics/salt_system_architecture.html)_
 * salt-minion:  boosted with ``asterisk_ami.py`` and ``odoo_executor.py`` engines.

OdooPBX Agent is designed to be as much auto provisioned as possible.
What you basically need is to run all these 3 services with ``ODOO_URL``
environment variable pointing to Odoo server with Asterisk Plus module installed.


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
