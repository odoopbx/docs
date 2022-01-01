:banner: banners/asterisk_plus.png

===
API 
===

Channels
========
Channel represents a point of communication. 

Fields
######
.. autoattribute:: odoo.addons.asterisk_plus.models.channel.Channel.call
.. autoattribute:: odoo.addons.asterisk_plus.models.channel.Channel.server

Methods
#######

.. automethod:: odoo.addons.asterisk_plus.models.channel.Channel.on_ami_new_channel

.. automethod:: odoo.addons.asterisk_plus.models.channel.Channel.on_ami_update_channel_state

.. automethod:: odoo.addons.asterisk_plus.models.channel.Channel.on_ami_hangup


Servers
=======

.. automodule:: odoo.addons.asterisk_plus.models.server


Channels
========

.. automodule:: odoo.addons.asterisk_plus.models.user_channel


Res Users
=========

.. automethod:: odoo.addons.asterisk_plus.models.res_users.ResUser.asterisk_plus_notify

PBX User
========

.. automethod:: odoo.addons.asterisk_plus.models.user.PbxUser.has_asterisk_plus_group