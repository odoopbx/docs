====================
IAX2 interconnection
====================
Introduction
============
Sometimes it is required to interconnect two Asterisk servers. 

Currently Asterisk Base does not support IAX2 peers (only SIP is supported by the UI).

But this is no a problem at all as you always have the possibility to enter the .conf files
and configure whatever is required.

This document covers this topic.

IAX2 channel configuration
==========================
First you should tell Asterisk to load the chan_iax.so driver.

Unmask the module
#################
By default Asterisk Base has a ``modules.conf`` with ``chan_iax2.so`` loading masked:

.. code:: 

    [modules]
    autoload=yes
    ...
    noload => chan_iax2.so
    ...

You should either comment this line out and make like this:

.. code:: 

    [modules]
    ; autoload=yes
    ...
    noload => chan_iax2.so
    ...

Create the IAX2 conf file
#########################
Go to ``PBX -> Files`` and create a new file named ``iax.conf`` with the following content:

.. code::

    [general]
    bindport=4569
    bindaddr=0.0.0.0
    delayreject=yes
    language=en
    disallow=all
    allow=alaw
    jitterbuffer=yes
    forcejitterbuffer=no
    maxjitterbuffer=200
    resyncthreshold=1000
    maxjitterinterps=10
    minregexpire = 60
    maxregexpire = 3600
    qualifyfreqok=60000
    qualifyfreqnotok=10000
    iaxthreadcount = 5
    authdebug=yes
    tos=ef
    autokill=yes
    codecpriority=caller

    [guest]
    type=user
    context=no-calls
    callerid="Guest IAX User"

Make sure you have a ``guest`` section that has a context pointing to a non-routable dialplan, for example:

.. code:: 

 [no-calls]
 exten => _X!,1,Hangup()

Define your IAX2 trunk
======================

.. code::

    [techsupport]
    host=iax2.virtualpbx.ru
    type=friend
    context=from-techsupport
    secret=customer_pass
    username=customer_id
    callgroup=1
    pickupgroup=1
    callerid="Tech Support" <799>

