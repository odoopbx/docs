=======================
Docker based deployment
=======================
We use docker compose to define and run the OdooPBX services. The following services are defined:

* **db** - PostgreSQL database used by Odoo.
* **odoo** - Odoo server.
* **pbx** - A universal image with Asterisk amd Salt processes (salt-master, salt-minion, salt-api).
  The processeses are managed by Supervisor.
* **freepbx** - We use `tiredofit/freepbx <https://github.com/tiredofit/docker-freepbx>`_ - 
  the most popular FreePBX image published on the docker.hub. *Disclaimer: we do not maintain this FreePBX image.
  You can replace it with any other FreePBX docker image of your choice.* 

.. note::

  Take the `docker-compose.yml file  from the Agent repo <https://github.com/odoopbx/agent/blob/master/docker/docker-compose.yml>`_.

Also have a look at the `docker-compose.override.yml example <https://github.com/odoopbx/agent/blob/master/docker/docker-compose.override.yml.example>`_ 
on how to customize the defaults (save this file under ``docker-compose.override.yml`` name.)

Note that ``network_mode: host`` is used to connect the services to the host network so you can connect
to the localhost from inside containers.(usually Asterisk AMI is bound to 127.0.0.1:5038 that is good).

So depending on your required setup you can choose which services to run.

Below you will find some snippets for different environments.

Only Agent setup
================
This setup assumes that both Odoo and Asterisk are already installed and running outside docker.

So in this case you should do the following steps:

* Supply a configuration file for Odoo & Asterisk (see below).
* Change the default Sapt API password (not required but strictly recommended).

Let review these steps in more details.

Custom minion configuration file
################################
Here is an example of  ``minion_local.conf``:

.. code:: yaml

    odoo_db: my_database # Replace to your real Odoo database name.
    odoo_password: asterisk1password # Find in Settings -> Users asterisk1 user and set him a new password.
    odoo_port: 443
    odoo_use_ssl: True
    ami_login: odoo
    ami_secret: dfghj5678b
    ami_port: 5038
    ami_host: localhost # Your Asterisk host. Most common value is 127.0.0.1.

*This is an example of custom options. See the full list of possible options* - :doc:`../administration/params`.

Change the default Salt API password
####################################
The Salt API password is stored in ``/etc/salt/auth`` file. Generate a new password like that:

.. code:: bash

  echo -n "salt-api-new-pass" | md5sum

Save this password in ``auth`` file:

.. code::

  odoo|bf67d5d35021cb370bcbfb046f6c437f

Create docker-compose.override.yml
##################################
Next you need to map all these in ``docker-compose.override.yml``:

.. code:: yaml

    version: '3.1'
    services:

  pbx:
      volumes:
        - ./minion_local.conf:/etc/salt/minion_local.conf
        - ./auth:/etc/salt/auth
        - /var/spool/asterisk:/var/spool/asterisk
        - /etc/asterisk:/etc/asterisk
        - /var/run/asterisk:/var/run/asterisk
      environment:
        - ASTERISK_AUTOSTART=false

Now your are ready for a test run:

.. code:: sh

  docker-compose up pbx

Check the output. If there is no error messages, press CTRL+C and restart the Agent in background mode:

.. code:: sh

    docker-compose up -d pbx

Debug the Agent connection
##########################
Agent is built-up from three processes:

* Salt API
* Salt master
* Salt minion

The processes are started by the Supervisor daemon.

So in order to debug a process you first have to enter the container using

.. code::
  
  docker-compose exec pbx bash

Now stop the required process. Usually we want to debug the salt-minion process so we stop it and
run in debug mode:  

.. code::
  
  supervisorctl stop salt-minion
  salt-minion -l debug

You can press ``CTRL+C`` to terminate the process and restart again in normal mode:
.. code::

  CTRL+C
  supervisorctl stort salt-minion

Then you can exit the container with ``CTRL+d``.


Odoo
====
Coming soon.

Asterisk
========
Coming soon.

