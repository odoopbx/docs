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
  Also there is a ``tcp`` pre-configured transport, sometimes it's necessary to use this transport, for example for Microsoft Lync.

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

