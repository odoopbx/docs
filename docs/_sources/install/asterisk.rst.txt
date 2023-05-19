----------------------
Asterisk configuration
----------------------
.. warning::

  Network access to your Asterisk AMI / HTTP ports must be restricted!
  Make sure you open your AMI & HTTP ports only for the Agent IP address that is displayed in PBX -> Settings -> Server page.

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
    webenabled = no
    port = 5038
    bindaddr = 0.0.0.0 # Pay attention it binds to public interfaces so you must restrict access only to the Agent IP address.

    [odoo]
    secret=odoo # Make sure you change this password as per the OdooPBX server's configuration.
    allowmultiplelogin=no
    displayconnects = yes
    read=call,dialplan,user
    write=originate
    deny=0.0.0.0/0.0.0.0
    permit=x.x.3.4/255.255.255.255 # Put here Agent IP address. This IP address will be available from Odoopbx server settings after activating subscription.
    

Asterisk-based distributions such as **FreePBX**  offer a web GUI interface for managing your
AMI users. You can use that interface to create one, or you can add the account configuration data in
a custom file, which will not be managed by the distro, usually ``/etc/asterisk/manager_custom.conf``

.. warning::
   For security reasons always use deny/permit options in your manager.conf.
   Change permit option to IP address of the agent. 

Make sure that you applied new configuration by checking the Asterisk console:

.. code::
    
    manager show user odoo

Static HTTP server
------------------
Asterisk has a built-in static HTTP server that is used to get call recordings. 

To enable it the following steps shold be done:

* Configure http.conf to enable it.
* Create a symbolic link for the *monitor* folder.
* Restart the Asterisk and make a test. 

Configure http.conf
===================
The following options must be added there:

* enabled=yes
* enablestatic=yes
  
Symbolic link
=============
Usually call recordings are stored in ``/var/spool/asterisk/monitor`` and 
static root folder is ``/var/lib/asterisk/static-http/``.

Create the link like in the following example:

.. code:: bash

    cd /var/lib/asterisk/static-http/
    ln -s /var/spool/asterisk/monitor .

Make sure the link is correct:

.. code:: bash

    ls -l
    ...
    lrwxrwxrwx 1 root     root      27 Mar 16 10:45 monitor -> /var/spool/asterisk/monitor

Test
====
Get a recording name from the monitor folder:

.. code:: bash

  ls /var/spool/asterisk/monitor/ | head -1
  1b504b46-929b-4c2b-9ed4-28863d685bf3.wav

Now try to download this file from your browser (make sure HTTP access is open for your IP otherwise you'll get 403 Access Denied):

.. code::

    wget http://asterisk.host:8088/static/monitor/1b504b46-929b-4c2b-9ed4-28863d685bf3.wav

If you can get the file then HTTP server is setup correctly. Don't forget to restrict the access to it.

Troubleshooting
---------------
After the AMI account is created, you need to make sure that it's updated inside Asterisk configuration.
Open the Asterisk console using ``asterisk -r`` as root and see if the Odoo manager user is available:

.. code::

   > manager show user odoo

     username: odoo
     secret: <Set>
     ACL: yes
     read perm: call
     write perm: originate
     displayconnects: yes
     allowmultiplelogin: yes
     Variables:

If you don't see the user, maybe the AMI configuration file hasn't been read by Asterisk after being modified.
This can be solved by running inside the Asterisk console the command ``core reload``.
