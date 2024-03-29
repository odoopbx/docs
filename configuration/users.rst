=========
PBX Users
=========
PBX Users are Odoo users connected to Asterisk channels and extensions.

.. note::

    This mapping is used in the following cases:

    * When Odoo user clicks to call a number on a form - the system must know which SIP user channel
      to dial in order to connect the call.
    * When call events come into Odoo it must decide which user is related to the event.

Odoo user can have multiple channels defined for him. In a typical scenario user 
has a hardware deskphone and also a softphone with a headset. 

Normally user receives incoming calls on his desk phone.

But when a user wants to make a series of calls to partners it's much handy to use a headset and click to dial
function instead of manual phone number dialing.

Let's review channel settings:

Channel
-------
Asterisk channel, e.g. SIP/101 or SIP/mypeername

SIP Transport
-------------
Choose what transport to use for SIP account. 

.. note::
  Typically desktop softphones (MicroSIP, Zoiper, Linphone, etc) use ``udp``. Browser softphones (sipml5, sip.js, jssip) are for ``webrtc``.
  Also there is a ``tcp`` pre-configured transport, sometimes it's necessary to use this transport, e.g. for Microsoft Lync.

.. warning::
  In order to be able to choose transport template turn of ``Autocreate PBX Users`` and ``Autocreate PBX Users`` in `PBX -> Settings - Server`

Sample transport settings for ``pjsip.conf``

.. code::

    [transport-wss]
    type=transport
    protocol=wss
    bind=0.0.0.0:65060
    external_media_address={{your_server_ip}}
    external_signaling_address={{your_server_ip}}
    local_net=127.0.0.1/8
    allow_reload=true

    [transport-udp]
    type=transport
    protocol=udp    ;udp,tcp,tls,ws,wss
    bind=0.0.0.0:65060
    allow_reload=yes
    external_media_address={{your_server_ip}}
    external_signaling_address={{your_server_ip}}
    local_net=127.0.0.1/8

    [transport-tcp]
    type=transport
    protocol=tcp    ;udp,tcp,tls,ws,wss
    bind=0.0.0.0:65060
    allow_reload=yes
    external_media_address={{your_server_ip}}
    external_signaling_address={{your_server_ip}}
    local_net=127.0.0.1/8

Here are ``pjsip_wizard.conf`` templates for all transports

.. code::

    [webrtc-user](!)
    type = wizard
    transport = transport-wss
    accepts_registrations = yes
    sends_registrations = no
    accepts_auth = yes
    sends_auth = no
    endpoint/webrtc = yes
    endpoint/dtls_auto_generate_cert = yes
    endpoint/context = from-internal
    endpoint/allow = !all,alaw,ulaw
    endpoint/direct_media = no
    endpoint/force_rport = yes
    endpoint/rewrite_contact = yes
    endpoint/rtp_symmetric = yes
    endpoint/allow_transfer = yes
    endpoint/send_diversion = yes
    endpoint/ice_support = yes
    aor/qualify_frequency = 30
    aor/authenticate_qualify = no
    aor/max_contacts = 1
    aor/remove_existing = yes
    aor/minimum_expiration = 30
    aor/support_path = yes
    endpoint/inband_progress = yes

    [udp-user](!)
    type = wizard
    endpoint/rtp_symmetric=yes
    transport = transport-udp
    accepts_registrations = yes
    sends_registrations = no
    accepts_auth = yes
    sends_auth = no
    endpoint/context = from-internal
    endpoint/allow_subscribe = yes
    endpoint/allow = !all,ulaw,gsm,alaw
    endpoint/direct_media = no
    endpoint/force_rport = yes
    endpoint/ice_support = yes
    endpoint/moh_suggest = default
    endpoint/send_rpid = yes
    endpoint/rewrite_contact = yes
    endpoint/send_pai = yes
    endpoint/allow_transfer = yes
    endpoint/trust_id_inbound = yes
    endpoint/device_state_busy_at = 1
    endpoint/trust_id_outbound = yes
    endpoint/send_diversion = yes
    aor/qualify_frequency = 30
    aor/authenticate_qualify = no
    aor/max_contacts = 1
    aor/remove_existing = yes
    aor/minimum_expiration = 30
    aor/support_path = yes


    [tcp-user](!)
    type = wizard
    endpoint/rtp_symmetric=yes
    transport = transport-tcp
    accepts_registrations = yes
    sends_registrations = no
    accepts_auth = yes
    sends_auth = no
    endpoint/context = from-internal
    endpoint/allow_subscribe = yes
    endpoint/allow = !all,ulaw,gsm,alaw
    endpoint/direct_media = no
    endpoint/force_rport = yes
    endpoint/ice_support = yes
    endpoint/moh_suggest = default
    endpoint/send_rpid = yes
    endpoint/rewrite_contact = yes
    endpoint/send_pai = yes
    endpoint/allow_transfer = yes
    endpoint/trust_id_inbound = yes
    endpoint/device_state_busy_at = 1
    endpoint/trust_id_outbound = yes
    endpoint/send_diversion = yes
    aor/qualify_frequency = 30
    aor/authenticate_qualify = no
    aor/max_contacts = 1
    aor/remove_existing = yes
    aor/minimum_expiration = 30
    aor/support_path = yes


Context
-------
Asterisk context to use to place the outgoing call. In FreePBX  related systems it is usually ``from-internal``.
Some other systems define individual context for each user.

Originate
---------
If Originate slider is ``on`` the channel will be used on click to dial operation. Usually when user a deskphone
and a softphone only softphone channel has ``Originate`` enabled so that when click to dial is used the deskphone
does not ring.

Auto-answer header
------------------
Auto answer is a very important business feature. 

When click to dial is used to originate call to a partner Asterisk first makes
a call to user (1-st call leg) and after user answered his phone the 2-nd call leg
is originated to the partner number.

It is possible to auto answer the 1-st call leg using special channel headers.
Different phones use different headers.

.. seealso::
  For more details see :doc:`auto_answer`

