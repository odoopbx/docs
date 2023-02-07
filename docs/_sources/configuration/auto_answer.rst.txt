===========
Auto-Answer
===========

Introduction
============
Auto-answer is a phone feature that allows to automatically answer a call 
without any action by the user, such as pressing the Accept Call button.

Not all phones support auto-answer feature.

The auto-answer function can be of two types:

1. Auto-answer all calls (unconditional).
2. Auto-answer on condition.

For us only the 2-nd type is important because it is heavily used on click-to-dial operation.

.. warning:: 

  Do not confuse this with unconditional auto-answer, which automatically accepts all incoming calls,
  including from colleagues and partners. We are only interested in conditional
  auto-answer when the correct SIP header is set.

When you a click the dial button on the Odoo's partner form the following happens:

1. Asterisk receives Originate command to user's SIP channel (e.g. SIP/100).
2. When user answers Asterisk starts to place the call to the partner on provider's channel (e.g. SIP/provider/1234567890).

So without the auto-answer function when user clicks the dial button his phone rings and he has 
to click Accept call button. So one single call requires 2 clicks!

To make it one-click-operation special phones should be used that accept auto-answer feature based
on SIP header. In this case when click to dial button is pressed Odoo sets a **special auto-answer SIP header**
(every phone has his own header defined) and user's phone automatically accepts the first call leg.

From the point of view of the user when he clicks the partner's dial button he immediately can hear
call progress tone coming from his phone.

The auto-answer feature is set in ``PBX -> Users`` menu:

.. image:: media/user_auto_answer.png


Phones with auto-answer support
===============================

Zoiper
######
Only Zoiper paid editions supports auto-answer header. Here is its SIP header: ``Call-Info:<sip:>;answer-after=0``.

* Zoiper 5:  Zoiper Options window; Automation; Enable the "Accept server-side auto answer".

Microsip
########
MicroSIP will play short tone and popup.

SIP header: ``Call-Info: Auto Answer`` or ``Call-Info: answer-after=0`` or ``X-AUTOANSWER: TRUE``

Source - https://www.microsip.org/help

To be continued...
##################