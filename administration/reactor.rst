================
Security Reactor
================

Reactor Introduction
====================
In order to protect the Asterisk server a Security Reactor is implemented.

As most of the installations (at least for now) use an external Asterisk / FreePBX server the 
security reactor is not enabled by default.

To enable the reactor add ``ami_reactor_enabled: True`` to ``/etc/salt/minion_local.conf`` and restart
the minion.

Make sure that a ``voip`` chain is created in iptables and that the necessary ``ipsets`` are created:

.. code:: bash

    iptables -nL INPUT | grep voip
    ipset list

When the reactor is enabled all unsuccessful SIP registrations will cause the incoming IP address to be added to the ``banned`` ipset. 

You can check that manually using ``ipset list banned`` or though the Odoo UI in ``Settins -> Security -> Banned`` menu (use the Refresh button to first load the 
entries from the Agent).