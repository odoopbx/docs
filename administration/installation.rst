============
Installation
============

Introduction
============
This guide assumes that both Odoo and Asterisk are already installed and running.

Installation process consists of two parts:

* Odoo module installation.
* Asterisk Agent installation.

First install & configure the Odoo module and then install the Asterisk agent.

Odoo module installation
========================
Install Asterisk Plus module in the same way you install any other Odoo module.

Do a database backup before installation or upgrade and also make a backup of previous version of the module
if you have it (just in case to be able to restore quicky).


Requirements
############
The module dependencies are localed in ``requirements.txt`` file located in the module folder.

If you use odoo.sh make sure you copy the requirements to your modules top folder so that odoo.sh can 
install the required dependencies.

If you use python virtualenv make sure you install the requirements there and not system wide.


Configuration
#############
Odoo should be configured in the right way in order to be ready for Asterisk Plus.

Usually Odoo configuration file is located in ``/etc/odoo/odoo.conf`` but make sure
to use your environment configuration file.

Make sure that ``addons_path`` is set correctly to include Asterisk Plus modules.

Workers
+++++++
Workers are Odoo processes that handle requests.

Asterisk modules make many short-running requests.

So your Odoo should be configured with at least 2 workers 
(but 4 workers is the minimal recommended starting value).

.. warning:: 
    If you use odoo.sh with 1 worker configured it is possible to get issues related to performance.


Gevent process for long polling
+++++++++++++++++++++++++++++++
Internal gevent-based server must be enabled (aka long polling) for popup notifications
and live channels reload to work.

When you enable workers gevent server is also enabled.

By default port 8072 is used and you can check it with:

.. code::

    netstat -an | grep LISTEN | grep 8072

on your Odoo server.

If you don't use a proxy (apache / nginx / etc) then you should open Odoo
on gevent's port e.g.: ``http://127.0.0.1:8072/web``.

If you run Odoo behind a proxy be sure to add a different proxy handler for /longpolling/poll URL.

Here is a snippet for Nginx:

.. code::

    location /longpolling/poll {
      proxy_pass http://127.0.0.1:8072;
    }

If you see ``Exception: bus.Bus unavailable`` in your Odoo log then it means you
did not set long polling right.

Single / multi database setup
+++++++++++++++++++++++++++++
There is one thing your should know.

It's a good configuration when your Odoo is limited to just one database with dbfilter
configuration option and list_db set to False.

But when you run Odoo with multiple databases some special configuration must be enabled.

You should add asterisk_plus to **server_wide_modules** parameter in order to be able 
to make CURL requests from the Asterisk dialplan (see below).

Here is an example of such a configuration line:

.. code::

    server_wide_modules = web,asterisk_plus

The Asterisk Agent installation
===============================
The best place to install the Agent is the same server where Asterisk is running because in this case
it has direct access to local file system  and can access call recordings. 

If you don't need call recordings in Odoo you can setup the Asterisk agent on a different computer but
it is advised to place it near the Asterisk server.

It is also possible install the Agent into a virtual environment.

.. note:: 
    Please note that the Agent requires root privileges. The commands below must be run as the **root** user.

Installation on Ubuntu and Debian
#################################

.. code::

    apt update && apt -y install python3-pip python3-setproctitle
    pip3 install odoopbx

Installation on CentOS
######################

Versions 6&7
++++++++++++
First, you should enable and install Python3 and pip.

There are at least `3 ways to install the latest Python3 package on CentOS <https://www.2daygeek.com/install-python-3-on-centos-6/>`_. 

Below is one of them (IUS).

.. code:: 

    curl 'https://setup.ius.io/' -o setup-ius.sh
    sh setup-ius.sh
    yum --enablerepo=ius install python36 python36-pip python36-setproctitle
    pip3 install odoopbx

.. warning::

   Please note that if you are using FreePBX, which is based on Centos 7, it has a different Python3 naming schema,
   similar to ius, but using Sangoma's own repositories. You shouldn't try to use 3rd party repositories,
   simply run ``yum makecache`` to get latest information from Sangoma's repositories and install Python3 by running 
   ``yum install python36u python36u-pip``

Version 8
+++++++++
Latest CentOS is quite ready for Python3. So here are the installation steps:

.. code::

    yum install python3 python3-pip python3-devel
    pip3 install odoopbx


Sangoma Linux release 7.8
#########################

.. code::

    yum install python36u python36u-pip python36u-devel
    pip3.6 install odoopbx
    

Installation error
##################
During ``odoopbx install agent`` execution the following log lines are expected and they are normal:

.. code::
 
 14:16:12 - salt.loaded.ext.module.asteriskmod:40 - ERROR - ipsetpy lib not found, asterisk module not available.
 14:16:12 - salt.loaded.ext.module.odoomod:23 - INFO - OdooRPC lib not found, odoo module not available.

This is because these packages are going to be installed exactly during this operation.

The Asterisk Agent initialization
=================================
After odoopbx utility has been installed it is necessary to initilize the Asterisk Agent.

.. code:: sh

    root@dev# odoopbx init
    Initializing salt minion ID [760e0474-dd50-4cf9-8f04-26b3ee4a4245]
    Minion [760e0474-dd50-4cf9-8f04-26b3ee4a4245] ready to go

    


Asterisk AMI configuration
==========================
You should prepare an Asterisk Manager Interface (AMI) account to allow the Agent to connect to Asterisk.

Vanilla Asterisk requires editing the  ``manager.conf`` file, which is usually found in ``/etc/asterisk``.

A sample configuration is provided below, which lets the Agent to connect
to your Asterisk server AMI port (usually 5038) using the login ``odoo`` with the password ``odoo``.


``manager.conf``:

.. code::

    [general]
    enabled = yes
    webenabled = no ; Asterisk calls does not use HTTP interface
    port = 5038
    bindaddr = 127.0.0.1

    [odoo]
    secret=odoo
    displayconnects = yes
    read=all
    write=all
    deny=0.0.0.0/0.0.0.0
    permit=127.0.0.1/255.255.255.0

Asterisk-based distributions such as **FreePBX**  offer a web GUI interface for managing your
AMI users. You can use that interface to create one, or you can add the account configuration data in
a custom file, which will not be managed by the distro, usually ``/etc/asterisk/manager_custom.conf``

.. warning::
   For security reasons always use deny/permit options in your manager.conf.
   Change permit option to IP address of your Asterisk server if agent is not started on the same box. 

Make sure that you applied new configuration by checking the Asterisk console:

.. code::
    
    manager show user odoo


The Agent Configuration
=======================
The Agent local configuration file is located in ``/etc/salt/minion_local.conf``.

The defaults are located in ``/etc/salt/minion.d/odoopbx.conf``.

When you add an option to the local configuration it overwrites the default value.

Odoo settings
#############
First configure the Agent's connection to Odoo:

.. code::

    odoopbx config set odoo_host 1.2.3.4 # Put IP address or hostname here.
    odoopbx config set odoo_port 8069 # If your Odoo is behind a proxy put 80 or 443 here.
    odoopbx config set odoo_bus_port 8072 # If your Odoo is behind a proxy put 80 or 443 here.
    odoopbx config set odoo_db demo # Put your database here
    odoopbx config set odoo_user asterisk # It's ok to leave the default user name.
    odoopbx config set odoo_password asterisk # This is the default password set on addon installation. CHANGE IT!!!
    odoopbx config set odoo_single_db false # Set to true if you have dbfilter or just one db.
    odoopbx config set odoo_use_ssl false # Set to true if your proxy servers HTTPS requests.

Asterisk AMI settings
#####################
Next we should configure the Agent for Asterisk connection.
Make sure you applied the Asterisk manager configuration first. 

Once you are sure the Odoo AMI user is operational run the following commands
to configure the Agent's connection
to your Asterisk:

.. code::

    odoopbx config set ami_host 127.0.0.1
    odoopbx config set ami_port 5038
    odoopbx config set ami_login odoo # Put here AMI user name you created in manager.conf.
    odoopbx config set ami_secret odoo # Put here AMI user password.

See ``/etc/salt/minion_local.conf`` to check that everything looks like expected.

Agent test run
==============

.. code::

    ; Stop the Agent service
    odoopbx stop agent
    ; Run in foreground
    odoopbx run agent

Check the Agent output printed on the screen. There should be no errors on start.

You should see messages that confirm both Odoo connection and Asterisk connection as shown below:

.. code::

   [INFO    ] salt.loaded.ext.engines.odoo_executor:48 Logged into Odoo.
   * * *
   [INFO    ] salt.loaded.ext.engines.asterisk_ami:69 AMI connecting to odoo@127.0.0.1:5038...
   [INFO    ] salt.loaded.ext.engines.asterisk_ami:72 Registering for AMI event *


Asterisk Dialplan configuration
===============================

Asterisk Plus exposes additional functionality by providing the following controllers:

#. You can get the contact's name by accessing ``asterisk_plus/get_caller_name?number=${CALLERID(number)}``
#. If the Contact for the phone number has a manager set, use ``asterisk_plus/get_partner_manager?number=${CALLERID(number)}`` to get the manager's number
#. You can get the Contact's tags by using ``/asterisk_plus/get_caller_tags?number=${CALLERID(number)}``

Here are some examples of integration, using Asterisk dialplans.


``extensions.conf``:

.. code::

    [globals]
    ODOO_URL=http://odoo:8069

    ; Set connection options for curl.
    [sub-setcurlopt]
    exten => _X.,1,Set(CURLOPT(conntimeout)=3)
    exten => _X.,n,Set(CURLOPT(dnstimeout)=3)
    exten => _X.,n,Set(CURLOPT(httptimeout)=3)
    exten => _X.,n,Set(CURLOPT(ssl_verifypeer)=0)
    exten => _X.,n,Return

    ; Partner's extension click2call e.g. +1234567890##101
    [post-dial-send-dtmf]
    exten => s,1,NoOp(DTMF digits: ${dtmf_digits})
    same => n,ExecIf($["${dtmf_digits}" = ""]?Return)
    same => n,Wait(${dtmf_delay})
    same => n,SendDTMF(${dtmf_digits})
    same => n,Return


    ;Set Caller ID name from Odoo
    ; Get caller ID name from Odoo, replace odoo to your Odoo's hostname / IP address
    ; Arguments:
    ; - number: calling number, strip + if comes with +.
    ; - db: Odoo's database name, ommit if you have one db or use dbfilter.
    ; - country: 2 letters country code, See https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    ; If country code is omitted Asterisk Agent's Odoo account's country settings will be used for phonenumbers parsing.
    
    [sub-setcallerid]
    exten => _X.,1,Gosub(sub-setcurlopt,${EXTEN},1)
    ;   You need to cut leading + on numbers incoming from trunks before passing it to get_caller_name.
    exten => _X.,n,Set(CALLERID(name)=${CURL(${ODOO_URL}/asterisk_plus/get_caller_name?number=${CALLERID(number)})})
    exten => _X.,n,Return


    ; Get partner’s manager (salesperson) channel

    [sub-dialmanager]
    exten => _X.,1,Set(manager_channel=${CURL(${ODOO_URL}/asterisk_plus/get_partner_manager?number=${CALLERID(number)})})
    exten => _X.,n,ExecIf($["${manager_channel}" != ""]?Dial(${manager_channel}/${EXTEN},60,t))
    exten => _X.,n,Return
    
    ; Get partner's tags to create a special call routing (e.g. VIP queue)
    ; You can also get caller tags from Odoo with the following controller Here is an example:
    
    ; Partner tags
    ; VIP - tag name in this example.

    [partner-vip-tag-lookup] 
    exten => _X.,1,Set(CURLOPT(conntimeout)=3)
    exten => _X.,n,Set(CURLOPT(dnstimeout)=3)
    exten => _X.,n,Set(CURLOPT(httptimeout)=3)
    exten => _X.,n,Set(CURLOPT(ssl_verifypeer)=0)
    exten => _X.,n,Set(tags=${CURL(${ODOO_URL}/asterisk_plus/get_caller_tags?number=${CALLERID(number)})})
    exten => _X.,n,NoOp(Tags: ${tags})
    exten => _X.,n,Set(match=${REGEX("VIP" ${tags})})
    exten => _X.,n,NoOp(Match: ${match})
    exten => _X.,n,Return(${match})

    ; Check VIP tag
    [check-vip]
    exten => _X.,1,Gosub(partner-vip-tag-lookup,${EXTEN},1,VIP)
    exten => _X.,n,GotoIf($["${GOSUB_RETVAL}" = "1"]?vip-queue,${EXTEN},1)


    ; Incoming call handling

    [from-sip-external]    
    exten => _X.,1,Gosub(sub-setcallerid,${EXTEN},1) ; Set partner's caller name    
    exten => _X.,n,MixMonitor(${UNIQUEID}.wav) ; Record call    
    exten => _X.,n,Gosub(sub-dialmanager,${EXTEN},1) ; Try to connect to manager
    ; Put here some login to handle if manager channel is busy for example put in the queue.
    exten => _X.,n,Queue(sales)

    [from-internal]
    exten => _X.,1,MixMonitor(${UNIQUEID}.wav) ; Activate call recording.
    exten => _XXXX,2,Dial(SIP/${EXTEN},30) ; Local users calling    
    exten => _XXXXX.,2,Dial(SIP/provider/${EXTEN},30,TU(post-dial-send-dtmf) ; Outgoing calls pattern

That's all for now!
