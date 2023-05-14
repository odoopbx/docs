-------------------------
OdooPBX demo installation
-------------------------

Odoo Docker depoyment
---------------------
To setup a demo Odoo CRM with Asterisk Plus module installed use the following ``docker-compose.yml`` file:

.. code:: yaml

  version: '3'
  services:
  odoo:
      image: odoopbx/odoo
      command: odoo -d odoopbx --workers=3 -i asterisk_plus,crm
      ports:
          - 8069:8069
          - 8072:8072
      depends_on:
          - db
      environment:
          - USER=odoo
          - PASSWORD=odoo
          - ODOO_HTTP_SOCKET_TIMEOUT=10
      volumes:
          - odoo_data:/var/lib/odoo
  db:
      image: postgres:12
      volumes:
          - db_data:/var/lib/postgresql/data/pgdata
      environment:
          - POSTGRES_USER=odoo
          - POSTGRES_PASSWORD=odoo
          - PGDATA=/var/lib/postgresql/data/pgdata

  volumes:
      db_data:
      odoo_data:

Start this docker compose and use your browser to visit Odoo on port 8072:

.. code:: 

    http://docker.host.address:8072/

Asterisk connection
-------------------
Check :doc:`install/asterisk` on how to configure your Asterisk server for Asterisk Plus module.

Demo subscription
-----------------
Visit `apps.odoopbx.com <https://apps.odoopbx.com>`__ and get a trial subscription code.

Use it to activate your instance in Odoo ``PBX -> Settings -> Server``.


Production
----------
You can use our Odoo docker image for production. To do this you should do the following:

* Create your custom odoo.conf and map it into Odoo container. This configuration should define
  the following:

  * Disable loading of demo data.
  * Set Odoo database administrator password.
  * Disable database listing (optionally).
  * Set number of worker twice more then you have CPU cores.

* Remove custom command from the ``docker-compose.yml`` not to update on every start.
* Setup a HTTPS proxy using Nginx or similar. For more information see :doc:`../install/odoo`.

Here is an example of odoo.conf:

.. code::

    [options]
    addons_path = /mnt/extra-addons
    admin_passwd = set-your-db-admin-pass
    list_db = False
    proxy_mode = True
    xmlrpc_interface = 0.0.0.0
    xmlrpc_port = 8069
    gevent_port = 8072
    without_demo = all
    workers = 4
    max_cron_threads = 2
    server_wide_modules = base,web

Map the file above inside your container (a snippet from the ``docker-compose.yml``):

.. code: yaml

    volumes:
    - odoo_data:/var/lib/odoo
    - ./odoo.conf:/etc/odoo/odoo.conf

