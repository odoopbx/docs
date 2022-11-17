========
Settings
========

Admin user
==========
During the installation process the ``admin`` user is automatically added to Asterisk Admin security group.

.. note::
  Do not add ``admin`` to Asterisk User security group!


PBX Settings
============

General
-------
Debug mode
++++++++++
When it is required to trace some issue enable the debug mode. 

When debug mode is enabled 


Salt
----
Here the Salt connection is configured. In the common setup all three Salt processes (master, api and minion) are running on the same server.

Salt API URL
++++++++++++
URL of the Salt Master. By default ``https://agent:48008``. Replace ``agent`` with the hostname of your Agent.

Salt API User & Password
++++++++++++++++++++++++
To generate new password use the following command:

.. code:: bash

  echo -n my-new-pass | md5sum
  7ee84110eed69ed3d366eb85e017b508  -

Now use this hash to edit ``/etc/salt/auth`` file and put it there:

.. code::

  odoo|7ee84110eed69ed3d366eb85e017b508

After that restart the salt minion service (``systemctl restart salt-minion``). Now set username ``odoo`` and password ``my-new-pass`` as Salt credentials in Odoo.

