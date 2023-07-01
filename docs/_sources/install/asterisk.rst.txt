===================
The middlware Agent
===================
This documentation assumes that the following components are already installed:

* Odoo: Odoo is already deployed and properly configured (see :doc:`odoo`).
* Asterisk: Asterisk PBX is also deployed and AMI account is configured (see :doc:`asterisk`).

Now the Agent middlware should be installed to connect them together.

The Agent does the following jobs:

* Forwards Asterisk events to Odoo according to the downloaded events map.
* Executes Asterisk actions received from Odoo.
* Protects Asterisk from DDoS and password bruteforce attacks (if enabled).

The best place to install the Agent is **the same server** where Asterisk runs because in this case
it has direct access to local file system  and can access call recordings and forward it into Odoo.

If you don't need call recordings in Odoo you can setup the Asterisk agent on a different computer but
it is advised to place it at least near the Asterisk server. But depending on your company size you can also
have your Asterisk in America and Odoo in Europe datacenter.

The Agent middleware
====================
The Agent middleware is based on the Nameko microservices framework and uses RabbitMQ server as the internal
message broker. 

Also it uses Nginx Proxy Manager (NPM) to add SSL encryption layer to the communication between
Odoo and the Agent. After the installation open your server's address in the WEB browser on port ``81`` and
configure the NPM host. Set it either to IP address or DNS hostname.

After that you go to Odoo and enter there the Agent URL. Here is an example:

* Agent URL: https://x.x.x.x/rpc/


Use the following ``docker-compose.yml`` file to deploy:

.. code:: yaml

    version: '3'
    services:

        agent:
            image: odoopbx/middleware
            restart: unless-stopped
            network_mode: host
            depends_on:
              - rabbitmq
            volumes:
              - /etc/asterisk:/etc/asterisk/
              - /var/spool/asterisk:/var/spool/asterisk
              - /var/run/asterisk:/var/run/asterisk
            environment:
              - ODOO_URL=https://your.odoo.addr
              - ODOO_DB=odoopbx_15
              - ODOO_USER=asterisk1
              - ODOO_PASSWORD=asterisk1
              # - ODOO_IP=1.2.3.4 # Optionally restrict access to only Odoo's IP address.
              - ASTERISK_AMI_USER=odoo
              - ASTERISK_AMI_PASSWORD=odoo
              - ASTERISK_AMI_HOST=localhost
              - TZ=Europe/London
              - AMQP_URI: pyamqp://guest:guest@localhost

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

        rabbitmq:
            image: rabbitmq
            ports:
               - "127.0.0.1:5672:5672"

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