===============
Asterisk Server
===============
Buttons
=======
* **Minion and Asterisk ping** - to check the connection between Odoo and Asterisk use the following buttons:
* **Console** - open WEB console in a separate browser tab. Make sure that your browser settings do not block new tabs.
* **Upload .conf files** - send the .conf files to the Asterisk server from Odoo. All existing on Asterisk .conf files will be overwritten.
* **Download .conf files** - download the .conf files from the Asterisk server to Odoo. All existing in Odoo .conf will be overwritten.
* **Reload** - issue the ``reload`` command to the Asterisk server.
* **Restart** - reboot the Asterisk server.

Settings
========
Asterisk system account
-----------------------
.. note:: 
  During the installation process **a new odoo account is created** named ``asterisk1`` with default password ``asterisk1``.  

This account is used by the Agent to connect to your Odoo instance. Don't use this account for anything else!

Though the permissions of this Asterisk user account are very limited (it belongs to the Portal group)
it is **strictly recommended** to change the default password of this account after installation is finished
(don't forget to update ``odoo_password`` setting on the Agent).

You can change the password of the Asterisk account by entering a new value in the ``Password`` field.

Country settings and timezone
-----------------------------
It is important to set the correct country for the Asterisk server because it is required to
correctly process caller ID numbers that usually come in local format.

Internally all partner numbers in Odoo are stored in E.164 format. So country settings are used to
correctly transform numbers from local to E.164 format.

Also server's timezone must be correctly set in order to correctly process times in calls.

Console URL
-----------
In order to connect to the Asterisk console you need to set the correct Agent WEB console URL. 

The WEB console service is provided by the ``asterisk_cli`` engine of the salt-minion process. 
So in the host part of the URL enter your Agent hostname or IP address.

By default port 30000 is used and self-signed certificates are generated. So if you use the defaults
you need to allow this self-signed certificate in your browser by opening first the console URL in
your browser and adding the permission.

Server startup
--------------
When Asterisk server is started its configuration files need to be syncronized with Odoo.

When the Asterisk server is connected to Odoo for the first time all its .conf files are sent to Odoo and ``Initial Update Done`` is set to ``True``.
If Odoo already has a file with the same name that is being sent, that file is not overwritten. 

After the initial configuration is done the correct update direction option must be set.

* **Odoo** -> Asterisk (Odoo is the source of configuration) - usually when you use a vanilla Asterisk server you manage this server from Odoo.
* **Asterisk** -> Odoo (Asterisk is the source of configuration) - when you use a third-party Asterisk distibution (for example, FreePBX based) it has its own management UI ahat generates .conf files.

Commands
========
This feature is for advanced users only :-)

It is possible to execute Salt commands on the Asterisk server. In order to do it you should enter
the edit mode of the server form and issue a command and use ``Tab`` button to take of the focus.

Then the command is sent to the Salt minion and the result is displayed in the Reply field.

You can try the following commands:

.. code::
    
    ps.cpu_percent
    ps.disk_usage
    ps.netstat
    ps.netstat name=asterisk
    ps.top
    ps.psaux name=salt
    network.get_fqdn
    network.ping host=odoopbx.com
    network.interface iface=eth0

The full list of possible commands can be found `here <https://docs.saltproject.io/en/latest/ref/modules/all/index.html>`__.

