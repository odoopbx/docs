=======================
Docker based deployment
=======================
We use docker compose to define and run the OdooPBX services. The following services are defined:

* **db** - PostgreSQL database used by Odoo.
* **odoo** - Odoo server.
* **agent** - Salt processes (salt-master, salt-minion, salt-api).
* **asterisk** - a plain Asterisk PBX with minimal set of configuration files.
* **freepbx** - We use `tiredofit/freepbx <https://github.com/tiredofit/docker-freepbx>`_ - 
  the most popular FreePBX image published on the docker.hub. *Disclaimer: we do not maintain this FreePBX image.
  You can replace it with any other FreePBX docker image of your choice.* 

You can take an example of ``docker-compose.yml`` file  from the Agent repo `here <https://github.com/odoopbx/docker/blob/master/docker-compose.yml>`_.

Also please note the ``docker-compose.override.yml`` example on how to customize the defaults: `here <https://github.com/odoopbx/docker/blob/master/docker-compose.override.yml.example>`_.

So depending on your requered setup you can choose which services to run.

Below you will find some snippets for different environments.

Only Agent setup
================
This setup assumes that both Odoo and Asterisk are already installed and running outside docker.

So when Odoo & Asterisk / FreePBX exists you require to supply a configuration file for Odoo & Asterisk. Here is an example:

``minion_local.conf``:

.. code:: yml

    odoo_db: my_database
    odoo_password: asterisk1password
    odoo_port: 443
    odoo_use_ssl: True
    ami_login: odoo
    ami_secret: dfghj5678b
    ami_port: 5038
    ami_host: asterisk.host

*Below is an example of custom options. See the full list of possible options* - :doc:`agent_options`.

Next you need to map this file in ``docker-compose.override.yml``:

.. code:: yml

    version: '3.1'
    services:

    minion:    
    volumes:
      - ./minion_local.conf:/etc/salt/minion_local.conf

Now your are ready for a test run:

.. code:: sh

  docker-compose up agent

Check the output. If there is no error messages, press CTRL+C and restart the Agent in background mode:

.. code:: sh

    docker-compose up -d agent



