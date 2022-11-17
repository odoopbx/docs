==========================
User interface actions API
==========================

Introduction
============
In order to perform some real time actions like opening partner'a form on incoming call or associated lead
or reload current active calls list there is a special API developed called UI Actions.

UI Actions are based on Odoo's built-in communication bus (``bus.bus``). See ``asterisk_plus/static/src/js/actions.js``
for details. 

When Odoo's Web client is loaded it starts to poll two channels:

* **asterisk_plus_actions** - this is used for performing different actions (see below). All users receive these actions.
* **'asterisk_plus_actions_' + session.uid** - this is an individual channel for user.

Action structure
================
Every action is a dictionary with one required key: ``action`` with value specifying the exact action.

Currently the following actions are defined:

* **notify** - used to send a notification message to user.
* **reload_view** - used to reload active calls list and call history views.
* **open_record** - used to open a partner form or CRM lead.

Notify
######
Example action:

.. code:: python

  {
    'action': 'notify',
    'title': 'PBX',
    'sticky': False,
    'warning': False,
    'message': 'Message text...'
  }

There is a special function that can be used to send notifications.

.. code:: Python

  self.env['res.users'].asterisk_plus_notify('Hello world!')

