===============
Troubleshooting
===============

Minion ID
=========
If you try to ping the minion from Odoo and nothing happens (and you don't see any changes in the 
minion's log) check the minion ID as set in Odoo and ``/etc/salt/minion_id``.

Asterisk connection
===================
After the AMI account is created, you need to make sure that it's updated inside Asterisk configuration.
Open the Asterisk console using ``asterisk -r`` as root and see if the Odoo manager user is available:

.. code::

   > manager show user odoo

     username: odoo
     secret: <Set>
     ACL: yes
     read perm: system,call,log,verbose,command,agent,user,config,dtmf,reporting,cdr,dialplan,originate,agi,cc,aoc,test,security,message,all
     write perm: system,call,log,verbose,command,agent,user,config,dtmf,reporting,cdr,dialplan,originate,agi,cc,aoc,test,security,message,all
     displayconnects: yes
     allowmultiplelogin: yes
     Variables:

If you don't see the user, maybe the AMI configuration file hasn't been read by Asterisk after being modified.
This can be solved by running inside the Asterisk console the command ``core reload``.
