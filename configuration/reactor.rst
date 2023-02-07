================
Security Reactor
================

Reactor Introduction
====================
In order to protect the Asterisk server a Security Reactor is implemented and enabled by default.

If any SIP user enters a wrong password his IP address is immediatly blocked on the firewall.

The Reactor is managed from the Odoo PBX -> Settings -> Security menu.

To disable the reactor set ``ASTERISK_SECURITY_ENABLED`` environment variable to ``no`` and restart the Agent.

Make sure that a ``voip`` chain is created in iptables and that the necessary ``ipsets`` are created:

.. code:: bash

    iptables -nL INPUT | grep voip
    ipset list

When the reactor is enabled all unsuccessful SIP registrations will cause the incoming IP address to be added to the ``banned`` ipset. 

You can check that manually using ``ipset list banned`` or though the Odoo UI in ``Settins -> Security -> Banned`` menu (use the Refresh button to first load the 
entries from the Agent).
