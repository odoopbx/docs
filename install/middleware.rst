========================================
The OdooPBX middlware Agent installation
========================================
This documentation assumes that the following components are already installed:

* Odoo: Odoo is already deployed.
* Asterisk: Asterisk PBX is also deployed.

Now the Agent middlware should be installed to connect them together.

The Agent does the following jobs:

* Forwards Asterisk events to Odoo according to the downloaded events map.
* Executes Asterisk actions received from Odoo.
* Protects Asterisk from DDoS and password bruteforce attacks.

The best place to install the Agent is the same server where Asterisk runs because in this case
it has direct access to local file system  and can access call recordings and forward it into Odoo.

If you don't need call recordings in Odoo you can setup the Asterisk agent on a different computer but
it is advised to place it at least near the Asterisk server. But depending on your company size you can also
have your Asterisk in America and Odoo in Europe datacenter.

Odoo configuration
==================
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

Do a database backup before installation or upgrade and also make a backup of previous version of the module
if you have it (just in case to be able to restore quicky).

Make sure that ``addons_path`` is set correctly to include OdooPBX addons.

The module dependencies are localed in ``requirements.txt`` file located in the addons folder.

If you use odoo.sh make sure you copy the requirements to your modules top folder so that odoo.sh can 
install the required dependencies.

If you use python virtualenv make sure you install the requirements there and not system wide.

Asterisk
========
AMI account
-----------
Prepare an Asterisk Manager Interface (AMI) account to allow the Agent to connect to Asterisk.

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
    allowmultiplelogin=no
    displayconnects = yes
    read=all
    write=all
    deny=0.0.0.0/0.0.0.0
    permit=127.0.0.1/255.255.255.0
    permit=172.172.0.0/255.255.0.0 # Docker network

Asterisk-based distributions such as **FreePBX**  offer a web GUI interface for managing your
AMI users. You can use that interface to create one, or you can add the account configuration data in
a custom file, which will not be managed by the distro, usually ``/etc/asterisk/manager_custom.conf``

.. warning::
   For security reasons always use deny/permit options in your manager.conf.
   Change permit option to IP address of your Asterisk server if agent is not started on the same box. 

Make sure that you applied new configuration by checking the Asterisk console:

.. code::
    
    manager show user odoo


The Agent middleware
====================
The Agent middleware is based on the Nameko microservices framework and uses RabbitMQ server as the internal
message broker. 

Also it uses Nginx Proxy Manager (NPM) to add SSL encryption layer to the communication between
Odoo and the Agent. After the installation open your server's address in the WEB browser on port ``81`` and
configure the NPM host. Set it either to IP address or DNS hostname.

After that you go to Odoo and enter there the Agent URL and Console URL. Here is an example:

* Agent URL: https://x.x.x.x/rpc/
* Console URL: https://x.x.x.x/console/


Use the following ``docker-compose.yml`` file to deploy:

.. code:: yaml

    version: '3'
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
            - /etc/asterisk:/etc/asterisk/
            - /var/spool/asterisk:/var/spool/asterisk
            - /var/run/asterisk:/var/run/asterisk
            environment:
            - ODOO_URL=https://your.odoo.addr
            - ODOO_DB=odoopbx_15
            - ODOO_USER=asterisk1
            - ODOO_PASSWORD=asterisk1
            - AMI_USER=odoo
            - AMI_PASS=odoo
            - ASTERISK_AMI_HOST=localhost
            - TZ=Europe/London

        npm:
            image: odoopbx/npm
            restart: unless-stopped
            depends_on:
            - 
            ports:
            - 80:80
            - 81:81
            - 443:443
            volumes:
            - npm_data:/data
            - letsencrypt:/etc/letsencrypt

        rabbitmq:
            image: rabbitmq
            ports:
            - 127.0.0.1:5672:5672 # Bind to the localhost!

        volumes:
        letsencrypt:
        npm_data:

        networks:
        default:
            driver: bridge
            ipam:
            config:
            - subnet: 172.172.0.0/16


Now run it and do a Test Ping from the Odoo server's form.

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


Enjoy!