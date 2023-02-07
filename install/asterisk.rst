----------------------
Asterisk configuration
----------------------
AMI account
-----------
Prepare an Asterisk Manager Interface (AMI) account to allow the Agent to connect to Asterisk.

Vanilla Asterisk requires editing the  ``manager.conf`` file, which is usually found in ``/etc/asterisk``.

A sample configuration is provided below, which lets the Agent to connect
to your Asterisk server AMI port (usually 5038) using the login ``odoo`` with the password ``odoo``.


``manager.conf``:

.. code::

    [general]
    enabled = yes
    webenabled = no ; Asterisk calls does not use HTTP interface
    port = 5038
    bindaddr = 127.0.0.1

    [odoo]
    secret=odoo
    allowmultiplelogin=no
    displayconnects = yes
    read=all
    write=all
    deny=0.0.0.0/0.0.0.0
    permit=127.0.0.1/255.255.255.0
    permit=172.172.0.0/255.255.0.0 # Docker network

Asterisk-based distributions such as **FreePBX**  offer a web GUI interface for managing your
AMI users. You can use that interface to create one, or you can add the account configuration data in
a custom file, which will not be managed by the distro, usually ``/etc/asterisk/manager_custom.conf``

.. warning::
   For security reasons always use deny/permit options in your manager.conf.
   Change permit option to IP address of your Asterisk server if agent is not started on the same box. 

Make sure that you applied new configuration by checking the Asterisk console:

.. code::
    
    manager show user odoo


Troubleshooting
---------------
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
