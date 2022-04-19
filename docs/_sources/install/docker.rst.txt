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

You can take an example of `docker-compose.yml file  from the Agent repo <https://github.com/odoopbx/agent/blob/master/docker/docker-compose.yml>`_.

Also please note the `docker-compose.override.yml example <https://github.com/odoopbx/agent/blob/master/docker/docker-compose.override.yml.example>`_ 
on how to customize the defaults (save this file under ``docker-compose.override.yml`` name.)

So depending on your required setup you can choose which services to run.

Below you will find some snippets for different environments.

Only Agent setup
================
This setup assumes that both Odoo and Asterisk are already installed and running outside docker.

So in this case you should do the following steps:

* Forward Salt API port (default 48008) from your host machine to the agent container.
* Supply a configuration file for Odoo & Asterisk.
* Change the default Sapt API password.

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
    ami_host: asterisk.host # Your Asterisk host. Most common value is 127.0.0.1.

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

    agent:
      ports:
        - "0.0.0.0:48008:48008"
      volumes:
        - ./minion_local.conf:/etc/salt/minion_local.conf
        - ./auth:/etc/salt/auth

Now your are ready for a test run:

.. code:: sh

  docker-compose up agent

Check the output. If there is no error messages, press CTRL+C and restart the Agent in background mode:

.. code:: sh

    docker-compose up -d agent

Debug the Agent connection
##########################
Agent is built-up from three processes:

* Salt API
* Salt master
* Salt minion

The processes are started in a `tmux <https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/>`__ session.

So in order to debug a process you first have to enter the container using

.. code::
  
  docker-compose exec agent bash
  
command and then re-connect to a tmux session using

.. code::
  
  tmux a

command.  After that you can switch between three consoles:

*  ``CTRL+b 0`` - the Salt master
*  ``CTRL+b 1`` - the Salt API
*  ``CTRL+b 2`` - the Salt minion

You can press ``CTRL+C`` to terminate the process and restart it in in debug mode. For example, to 
start the salt minion in debug mode go console #2 and enter:

.. code::

  CTRL+C
  salt-minion -l debug

To exit from tmux enter ``CTRL+B d``. Then you can exit the container with ``CTRL+d``.


Odoo
====
Coming soon.

Asterisk
========
Coming soon.

