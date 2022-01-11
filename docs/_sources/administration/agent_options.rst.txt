=============
Agent options
=============

Introduction
============
The OdooPBX Agent configuration and data files are located in ``/etc/odoopbx/``.

The default options are located in ``/etc/odoopbx/minion.d/default.conf``.

Your local customized options are stored in ``/etc/odoopbx/local.conf``.

Most of local options can be set using ``odoopbx`` CLI utility.

See `Working with configuration`_ for more on this.

Working with configuration
==========================
Instead of editing the ``/etc/odoopbx/local.conf`` file directly it is recommended to use the ``odoopbx`` utility.

To use it without mistakes you should know that values passed to it are parsed 
as JSON so you can pass not only strings but lists,  dictionaries and boolean values.

Below is a little video that demonstrates some tricks with settings config values.

.. image:: media/odoopbx_config_set.gif

Description of agent modes of operation
=======================================

The agent can work in two modes of operation: HTTP mode and bus mode.
The Odoo connector is launched by the ``connector_enabled`` option.

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``connector_enabled``
     - ``True``
     - If True, the agent will connect to Odoo using either the bus or HTTP modes.

Bus configuration options
-------------------------

The bus mode requires that Odoo has longpolling properly configured. See the 
``Gevent process for longpolling`` section in the Odoo configuration documentation.

.. seealso::
  * :doc:`odoo`
  
In this mode, the agent uses the longpolling port of Odoo (which is usually on port 8072)
to create long lasting connections. Every request from the agent is sent to the bus table in 
the database and after the request is processed, Odoo responds back using the initial connection.
Just enabling the bus connector, along with correct authentication credentials for the Asterisk user 
in Odoo are sufficient.

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``connector_bus_enabled``
     - ``True``
     - Enables or disables the bus connector.
     
HTTP configuration options
--------------------------

The configuration of the HTTP mode is more complex. The HTTP mode is used for instances where 
longpolling isn't available, such as odoo.sh. The agent creates a web server on the 40000 port by
default, and Odoo is configured to send there the responses to agent's requests.

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``connector_http_enabled``
     - ``True``
     - Enables or disables the HTTP connector.
   * - ``connector_port``
     - ``40000``
     - The port on which the agent is listening for incoming connections.

On the Odoo side, you need to configure the correct parameters for the Odoo's connection to the agent,
as shown in the screenshot below. To do that, go to ``PBX`` -> ``Settings`` -> ``Agent``.

.. image:: media/http_agent.png
   :align: center
   :alt: HTTP mode configuration

Configuration options
=====================
This section is under construction that means not all options are documented yet.

Agent Network Settings
######################

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``agent_listen_address``
     - ``0.0.0.0``
     - The IP address used by the agent
   * - ``agent_ssl_key``
     - ``/etc/odoopbx/pki/current/privkey.pem``
     - The SSL key used by the agent. By default a new key is generated.
   * - ``agent_ssl_crt``
     - ``/etc/odoopbx/pki/current/fullchain.pem``
     - The certificate used by the agent. By default a self-signed certificate is generated based on the key generated above.


Asterisk manager interface (AMI) connection related options
###########################################################

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``ami_login``
     - ``odoo``
     - Asterisk Manager Interface login as configured in ``/etc/asterisk/manager.conf`` (usually there).
   * - ``ami_secret``
     - ``odoo``
     - Asterisk Manager Interface secret as configured in ``/etc/asterisk/manager.conf`` (usually there).
   * - ``ami_enabled``
     - ``true``
     - Start AMI connector when Agent starts.
   * - ``ami_host``
     - ``localhost``
     - Hostname or IP address of your Asterisk server
   * - ``ami_register_events``
     - ``'*'``
     - The list of events which should be registered by the agent. By default all the events are registered.
   * - ``ami_trace_events``
     - ``False``
     - Adds more detailed output about the events received from Asterisk via AMI
   * - ``ami_trace_actions``
     - ``False``
     - Adds more detailed output about the actions sent to Asterisk via AMI


Asterisk console service engine
###############################
This engine makes Asterisk console available from Odoo.

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``asterisk_binary``
     - ``/usr/sbin/asterisk``
     - Asbsolute path to the Asterisk executable. The service runs this binary to connect to Asterisk command socket to send commands.
   * - ``asterisk_options``
     - ``-vvvvvr``
     - Options added when connecting to Asterisk binary, like default verbose level.
   * - ``asterisk_cli_port``
     - ``30000``
     - TCP port to listen to. Odoo's WEB console widget connects to this port using websocket method.
       Make sure this port is accessible from outside.
   * - ``asterisk_cli_enabled``
     -  ``true``
     - Start the CLI service when Agent starts.
   * - ``asterisk_shell_enabled``
     -  ``false``
     - Enable ``!`` command from Asterisk console to enter Linux shell.


Asterisk FastAGI engine
#######################
This engine starts a FastAGI server that can be used by Asterisk.

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``fastagi_enabled``
     - ``false``
     - FastAGI server is not enabled by default. Set this to ``true`` to start it up.
   * - ``fastagi_tts_google_app_key_file``
     - ``/srv/odoopbx/google_key.json``
     - Path to Google API key. Read the :doc:`agent_options` for more details.
   * - ``fastagi_listen_address``
     -  ``127.0.0.1``
     - FastAGI server listen inteface. Leave default if you don't connect to it from another external Asterisk server.
   * - ``fastagi_listen_port``
     - ``4574``
     - FastAGI server listen port.


Odoo connection related options
###############################

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Option
     - Default
     - Description
   * - ``odoo_host``
     - ``localhost``     
     - Hostname or IP address of your Odoo server.
   * - ``odoo_port``
     - ``8069``     
     - Odoo port that is accessible to Agent. When you use a proxy server e.g. Nginx you should put ``80`` here or ``443`` if you use HTTPS.
   * - ``odoo_bus_port``
     - ``8072``     
     - Odoo longpolling port that is accessible to Agent. When you use a proxy server e.g. Nginx you should put ``80`` here or ``443`` if you use HTTPS.
   * - ``odoo_db``
     - ``odoopbx_14``     
     - The name of the Odoo database to which the agent connects. Fill in with your database's name.
   * - ``odoo_user``
     - ``asterisk``     
     - The username used for connecting to Odoo.
   * - ``odoo_password``
     - ``asterisk``     
     - The password used for connecting to Odoo. Check the `After Install Steps <https://docs.odoopbx.com/installation/after_install.html#change-default-password>`_ document about changing the agent's password.
   * - ``connector_enabled``
     - ``true``
     - Odoo connector engine process that enabled Odoo to send command to the Agent.
   * - ``odoo_use_ssl``
     - ``False``
     - If set to ``True``, the agent will protect the connections with SSL/TLS and will not accept unprotected requests
   * - ``odoo_single_db``
     - ``False``
     - Set to True if you have db filter or only one database to save a query on every request.
   * - ``odoo_refresh_token_seconds``
     - ``300``
     - Describes the frequency with which the agent updates its security token used for Odoo authentication.
   * - ``odoo_trace_rpc``
     - ``False``
     - Adds more detailed output about the RPC calls sent from the Agent to Odoo.
   * - ``odoo_trace_ami``
     - ``False``
     - Adds more detailed output about the AMI requests received from Odoo.

Logging
#######

.. list-table::
   :widths: 20 15 65
   :header-rows: 1
   
   * - Option
     - Default
     - Description
   * - ``log_level``
     - ``info``
     - Logging level. See `Salt logging documentation <https://docs.saltproject.io/en/latest/ref/configuration/logging/index.html#log-levels>`_ for details on valid field values.
   * - ``log_file``
     - ``file:///dev/log/LOG_LOCAL0``
     - File to which the agent logs are being sent
   * - ``log_fmt_logfile``
     - ``'[%(levelname)-8s] %(name)s:%(lineno)s %(message)s'``
     - The format in which the logs are being sent to the log file. See `Salt documentation on log-fmt-logfile <https://docs.saltproject.io/en/latest/ref/configuration/logging/index.html#log-fmt-logfile>`_ for details on valid formatting options
   * - ``log_fmt_console``
     - ``'%(asctime)s %(colorlevel)s %(name)s:%(lineno)s %(message)s'``
     - The format in which the logs are being sent to the log file. See `Salt documentation  on log-fmt-console <https://docs.saltproject.io/en/latest/ref/configuration/logging/index.html#log-fmt-console>`_ for details on valid formatting options