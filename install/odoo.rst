-----------------------------
Odoo Application Installation
-----------------------------
Odoo application requires a simple process for basic installation depending on your operating system.
The most commonly used distro is linux ubuntu. For straight forward installation, you can use this bash install `script <https://github.com/Yenthe666/InstallScript>`_.

Odoo configuration
------------------
Odoo should be configured in the right way in order to be ready for Asterisk Plus module.

Workers
-------
Workers are Odoo processes that handle requests.

Asterisk modules make many short-running requests.

So your Odoo should be configured with at least 2 workers 
(but 4 workers is the minimal recommended starting value).

.. warning:: 
    If you use odoo.sh with 1 worker configured it is possible to get issues related to performance.


Long polling
------------
Internal gevent-based server must be enabled (aka long polling) for popup notifications
and live channels reload to work.

When you enable workers gevent server is also enabled.

By default port 8072 is used and you can check it with:

.. code::

    netstat -an | grep LISTEN | grep 8072

on your Odoo server.

If you don't use a proxy (apache / nginx / etc) then you should open Odoo
on gevent's port e.g.: ``http://127.0.0.1:8072/web``.

If you run Odoo behind a proxy be sure to add a different proxy handler for the ``/longpolling/poll`` URL.

Here is a snippet for Nginx:

.. code::

    location /longpolling/poll {
      proxy_pass http://127.0.0.1:8072;
    }

If you see ``Exception: bus.Bus unavailable`` in your Odoo log then it means you
did not set long polling right.

Single / multi database setup
-----------------------------
There is one thing your should know.

It's a good configuration when your Odoo is limited to just one database with dbfilter
configuration option and list_db set to False.

But when you run Odoo with multiple databases some special configuration must be enabled.

You should add asterisk_plus to ``server_wide_modules`` parameter in order to be able 
to make CURL requests from the Asterisk dialplan (see below).

Here is an example of such a configuration line:

.. code::

    server_wide_modules = web,asterisk_plus

If your Odoo is in a single-mode setup there is no need to configure the ``server_wide_modules`` parameter.

Addons
======
Install `addons <https://github.com/odoopbx/addons>`_ in the same way you install any other Odoo module.

Make sure you do a database backup before installation or upgrade and also make a backup of previous version of the module
if you have it (just in case to be able to restore quicky).

Make sure that ``addons_path`` is set correctly to include OdooPBX addons. `E.g addons_path=/odoo/enterprise/addons,/odoo/odoo-server/addons,/odoo/custom/addons`.

The module dependencies are located in ``requirements.txt`` file located in the addons folder.

If you use odoo.sh make sure you copy the requirements to your modules top folder so that odoo.sh can 
install the required dependencies.

If you use python virtualenv make sure you install the requirements there and not system wide.

Incase the module dependencies are not properly loaded during the module installation, you can install them using the following command from the command line.

.. code::

         pip install phonenumbers

Troubleshooting
===============

I don't get popup notifications
===============================
The most likely you the long polling mode is not enabled.

Check ``workers`` settings in your ``odoo.conf``.

