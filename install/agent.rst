--------------------------------
Asterisk Plus Agent installation
--------------------------------

Automatic initialization
------------------------
We have created the ability to automatically configure the Agent for the most typical scenario.
The following requirements are necessary for its execution:

* Module asterisk_plus installed in Odoo.
* Instance is registered and a subscription is created.
* Asterisk configuration files are located in /etc/asterisk.
* Folder /etc/asterisk/manager.conf.d is created and in /etc/asterisk/manager.conf there is line ``#tryinclude => /etc/asterisk/manager.conf.d/*.conf``.

There are 2 ways to deploy Asterisk Plus Agent:

* docker
* pip3 (requires python3.9 and above)

If your Asterisk server cannot run neither docker nor python3 please contact us for installation assistance.

To start initialization procedure you should start the agent with ``init`` option:

.. code:: bash

  # Docker style, create an empty file otherwise docker will create a directory instead of a file.
  touch /etc/asterisk_plus_agent.yaml && docker run --rm --volume /etc/asterisk:/etc/asterisk \
    --volume /var/run/asterisk:/var/run/asterisk  \
    --volume /etc/asterisk_plus_agent.yaml:/etc/asterisk_plus_agent.yaml \
    --network=host odoopbx/agent init http://localhost:8069

  # We map /etc/asterisk folder so that initialization procedure can place AMI account under 
  # /etc/asterisk/manager.conf.d and /var/run/asterisk so that it can connect to the 
  # running Asterisk to check the configuration.

.. code:: bash

  # Direct installation from Pypi.
  pip3 install asterisk-plus-agent
  asterisk-plus-agent init http://localhost:8069


Replace ``localhost:8069`` to your Odoo instance WEB URL and run the commands above. 
You ``/etc/asterisk_plus_agent.yaml`` config.

.. warning::

  You can use --skip-ami-setup init option to just get API keys from Odoo and setup AMI account manually.

Here is an example of ``/etc/asterisk_plus_agent.yaml`` file:

.. code:: yaml

  ami_host: localhost
  ami_password: xxxxxxxxxxxxxx
  ami_port: 5038
  ami_user: asterisk_plus_agent
  odoo_user: asterisk1
  odoo_password: xxxxxxxxxxxxx
  odoo_url: https://odoo.server
  odoo_db: odoopbx_16
  api_key: xxxxxxxxxxxxxxxxx
  api_url: https://api.odoopbx.eu-central-1.odooist.com/
  instance_uid: xxxxxxxxxxxxxx


Now use the following command to run the Agent:

.. code:: bash

  docker run -d --name agent  --restart=unless-stopped --network=host \
    --volume /etc/asterisk_plus_agent.yaml:/etc/asterisk_plus_agent.yaml \
    -- volume /var/spool/asterisk:/var/spool/asterisk \
    odoopbx/agent:latest run
  docker logs agent

or

.. code:: bash
  
  asterisk-plus-agent run

Now you should be able to Ping the Agent and Asterisk.

You can reload the page and make sure Agent Initialized checkbox is set.
If you ever need to re-initialize the Agent unset it and repeat the procedure. 
 

Manual installation
-------------------

Prepare an Asterisk Manager Interface (AMI) account to allow the Agent to connect to Asterisk.

Vanilla Asterisk requires editing the  ``manager.conf`` file, which is usually found in ``/etc/asterisk``.

A sample configuration is provided below, which lets the Agent to connect
to your Asterisk server AMI port (usually 5038) using the login ``asterisk_plus_agent`` with the password ``odoo``.


``manager.conf``:

.. code::

    [general]
    enabled = yes
    webenabled = no
    port = 5038
    bindaddr = 127.0.0.1

    [asterisk_plus_agent]
    secret=odoo
    allowmultiplelogin=no
    displayconnects = yes
    read=call,dialplan,security
    write=originate,system
    deny=0.0.0.0/0.0.0.0
    permit=127.0.0.1/255.255.255.255
    

If you use PBX Users auto provision feature then enable also 'system' write privilege in
order to execute AMI Reload action.

Asterisk-based distributions such as **FreePBX**  offer a web GUI interface for managing your
AMI users. You can use that interface to create one, or you can add the account configuration data in
a custom file, which will not be managed by the distro, usually ``/etc/asterisk/manager_custom.conf``

.. warning::
   For security reasons always use deny/permit options in your manager.conf.
   Change permit option to IP address of the agent. 

Make sure that you applied new configuration by checking the Asterisk console:

.. code::
    
    manager show user asterisk_plus_agent


After creating an AMI account manually you can init Agent again using ``--skip-ami-setup`` flag enabled.
After Odoo initialization part is done, open ``asterisk_plus_agent.yaml`` config and add AMI
settings there like in the example below:

.. code:: yaml

  ami_host: localhost
  ami_password: 9013f239-2bcd-426e-82b1-c1d58b0c2f17
  ami_port: 5038
  ami_user: asterisk_plus_agent

Save the file, and run the Agent.


Troubleshooting
---------------
After the AMI account is created, you need to make sure that it's updated inside Asterisk configuration.
Open the Asterisk console using ``asterisk -r`` as root and see if the Odoo manager user is available:

.. code::

   > manager show user odoo

     username: odoo
     secret: <Set>
     ACL: yes
     read perm: call,dialplan
     write perm: originate
     displayconnects: yes
     allowmultiplelogin: no
     Variables:

If you don't see the user, maybe the AMI configuration file hasn't been read by Asterisk after being modified.
This can be solved by running inside the Asterisk console the command ``core reload``.

Support
-------
If you need any assistance or cannot use docker feel free to submit a support ticket at our `Helpdesk <https://odoopbx.com/helpdesk>`__.