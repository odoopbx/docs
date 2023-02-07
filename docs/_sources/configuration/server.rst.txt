===============
Asterisk Server
===============
Buttons
=======
* **Test and Asterisk ping** - to check the connection between Odoo and Asterisk use these buttons.

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

