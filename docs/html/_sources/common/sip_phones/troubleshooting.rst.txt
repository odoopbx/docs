====================================
SIP phone connection troubleshooting
====================================

Host & Port
===========
When you can't connect your SIP client to Asterisk make sure that you are using 
the correct protocol and port.

The default port used for SIP is 5060.

When connecting to a server that is listening on port 5060 you don't need to
specify your username with a port, for example 701@sip.example.com.

In case a non-standard port is used, like 5062 you need to specify
the port while configuring your SIP credentials: 701@sip.example.com:5062.

Credentials
===========
Make sure the credentials are correct.

When using Asterisk Base app the credentials for connecting your SIP client
are available on the ``Applications -> Peers page``.
The fields SIP name will be the username and SIP Secret the password.

Security ban
============
Make sure your IP address is not blocked by our agent.

If you have introduced incorrect credentials in your SIP client 
your IP address will be added into the blacklist after a failed registration attempt.

Go to ``Reports -> Banned`` and click on the ``Refresh`` button to check if your IP address has been banned.
If you find your IP address there, click on the ``Plus button`` next to it to add it to the whitelist.

You can also go to ``Applications -> Security`` to add your IP address to the whitelist initially.

In this case your IP address will always be accepted by Asterisk.

Peers syncronized
=================
Check that the peers that are created in Odoo were propagated to Asterisk.

If you have created your peers and didn't click on the Apply Changes button
it will be impossible for the created peers to register.

Go to ``Applications -> Files`` and check that there are no files when the Updated filter is applied.
