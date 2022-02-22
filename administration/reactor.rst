================
Security Reactor
================

Introduction
============
In order to protect the Asterisk server a Security Reactor is implmented.

As most of the installations (at least for now) use an external Asterisk / FreePBX server the 
security reactor is not enabled by default.

To enable the reactor add ``ami_reactor_enabled: True`` to ``/etc/salt/minion_local.conf`` and restart
the minion.

