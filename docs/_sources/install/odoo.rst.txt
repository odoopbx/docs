=====================
Odoo preconfiguration
=====================
Odoo should be configured correctly for Asterisk Plus module.

Requirements
============
Asterisk Plus uses `NATs <https://nats.io/>`__ technology to communicate with the Agent middleware so must be installed
before trying to install the Asterisk Plus module. 

Different Python versions use different Python NATs implementations:

* Odoo 10, 11, 12: Python < 3.7
* Odoo 13, 14, 15, 16: Python >= 3.7


Odoo version 10, 11, 12
-----------------------
These versions use the following NATs library: https://github.com/mcuadros/pynats.

It can be installed like in the example below:

.. code:: 

  # Odoo 10
  pip install https://github.com/mcuadros/pynats/archive/refs/heads/master.zip
  # Odoo 11, 12
  pip3 install https://github.com/mcuadros/pynats/archive/refs/heads/master.zip
  
Odoo version 13 and above
-------------------------
.. code:: 

  pip3 install nats-py


HTTPS Redirect
--------------
If you use Nginx or other proxy to automatically redirect from http to https make sure 
to use "308 Permanent Redirect" and not "301 Moved Permanently" otherwise the Agent will not be able
to connect.
This issue happens because of request body modification, for details see `HTTP / Redirections <https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections>`__.

Workers
-------
Workers are Odoo processes that handle requests.

Asterisk Plus module handles many short-running requests coming from Asterisk.

So your Odoo should be configured with at least 2 workers 
(but 4 workers is the minimum recommended).

.. warning:: 
    If you use odoo.sh with 1 worker configured it is possible to get issues related to performance.


Long polling
------------

.. _longpolling:

Internal gevent-based server must be enabled (aka long polling) for popup notifications
and live channels reload to work.

When you enable workers gevent server is also enabled.

By default port 8072 is used and you can check it with:

.. code::

    netstat -an | grep LISTEN | grep 8072

on your Odoo server.

If you don't use a proxy (apache / nginx / etc) then you should open Odoo
on gevent's port e.g.: ``http://127.0.0.1:8072/web``.

If you run Odoo behind a proxy be sure to add a different proxy handler for the ``/longpolling/poll`` URL
(and ``/websocket`` starting from Odoo 16.0).

Here is a snippet for Nginx:

.. code::
  
    # Odoo up to  15.0 version
    location /longpolling/poll {
      proxy_pass http://127.0.0.1:8072;
    }

    # Odoo from 16.0 version, check full config here - https://www.odoo.com/documentation/16.0/administration/install/deploy.html
    location /websocket {
      proxy_pass http://127.0.0.1:8072;
    }

If you see ``Exception: bus.Bus unavailable`` in your Odoo log then it means you
did not set long polling right.

Multi database setup
--------------------

If your Odoo is limited to just one database
(``dbfilter`` configuration option is set and ``list_db`` is set to False)
then you can skip this step.

Otherwise you should add asterisk_plus to ``server_wide_modules`` parameter in order to be able 
to make CURL requests from the Asterisk dialplan (see below).

Here is an example of such a configuration line:

.. code::

    server_wide_modules = base,web,asterisk_plus

Prepair a directory for a new addon
-----------------------------------
Preapair a folder where you will place Asterisk Plus module.
Make sure this folder is listed in ``addons_path`` configuration option.


Troubleshooting
---------------

I don't get popup notifications
===============================
The most likely you the long polling mode is not enabled or nginx proxy is not correctly setup for
long polling.

Check ``workers`` settings in your ``odoo.conf``.

