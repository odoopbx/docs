
==========
Demo setup
==========

.. important::
   Minimum 4GB RAM is required.


Create the following docker-commpose.yml file:

.. code:: yml

    version: '3.2'
    services:

    agent:
        image: odoopbx/middleware
        restart: unless-stopped
        depends_on:
        - rabbitmq
        # To manipulate host's ipsets.    
        privileged: true
        network_mode: host 
        volumes:
        - asterisk_etc:/etc/asterisk/
        - asterisk_spool:/var/spool/asterisk
        - asterisk_run:/var/run/asterisk
        environment:
        - ODOO_URL=http://localhost:8069
        - ODOO_DB=odoopbx_15
        - ODOO_USER=asterisk1
        - ODOO_PASSWORD=asterisk1
        - AMI_USER=odoo
        - AMI_PASS=odoo
        - ASTERISK_AMI_HOST=localhost
        - TZ=Europe/London

    asterisk:
        image: odoopbx/asterisk
        restart: unless-stopped
        network_mode: host
        volumes:
        - asterisk_etc:/etc/asterisk/
        - asterisk_spool:/var/spool/asterisk/
        - asterisk_run:/var/run/asterisk/

    npm:
        image: odoopbx/npm
        restart: unless-stopped
        ports:
        - 80:80
        - 81:81
        - 443:443
        volumes:
        - npm_data:/data
        - letsencrypt:/etc/letsencrypt

    odoo:
        image: odoopbx/odoo:15.0
        restart: unless-stopped
        depends_on:
        - db
        ports:
        - 8069:8069
        - 8072:8072
        volumes:
        - odoo_data:/var/lib/odoo
        environment:
        - USER=odoo
        - PASSWORD=odoo

    db:
        image: postgres:12
        volumes:
        - db_data:/var/lib/postgresql/data/pgdata
        environment:
        - POSTGRES_USER=odoo
        - POSTGRES_PASSWORD=odoo
        - PGDATA=/var/lib/postgresql/data/pgdata

    rabbitmq:
        image: rabbitmq
        ports:
        - 127.0.0.1:5672:5672 # Bind to the localhost!

    volumes:
    asterisk_etc:
    asterisk_spool:
    asterisk_run:
    letsencrypt:
    npm_data:
    odoo_data:
    db_data:

    networks:
    default:
        driver: bridge
        ipam:
        config:
        - subnet: 172.172.0.0/16


Enter ``docker-compose up`` and wait about 5-10 minutes until all services roll out and enter a normal working state.

Odoo listens at port ``8072``.

Point your browser to http://your.server.address:8072 and enter admin/admin as username/password.

In PBX -> Server set the following ``Agent`` and ``Console`` settings:

* Agent URL: https://172.172.0.1:48000
* Console URL: https://your.server.address:48001, where your.server.address - is the IP or hostname of your server where you installed the demo.

Now press ``Minion Ping``, ``Asterisk Ping`` buttons to check connectivity with Agent and Asterisk.

Finally, click the ``Sync Now`` button in the bottom left corner of the server's form.

Enjoy!

P.S. You can also open your browser at https://your.server.address:81 and create a production SSL based deploy.
