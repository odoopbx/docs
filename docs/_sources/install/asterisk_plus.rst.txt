=============
Asterisk Plus
=============

This article explains how to install ``Asterisk Plus`` Odoo addon from `OdooPBX <http://odoopbx.com>`_.

Install the addon in Odoo
=========================
First, download the addon from the `Odoo market <https://apps.odoo.com/apps/modules/16.0/asterisk_plus/>`_.

Install the addon as any other Odoo module, refer to `Odoo documentation <https://www.odoo.com/documentation/16.0/applications/general/apps_modules.html#>`_
for details if needed.

Install python requirements
---------------------------
Install python dependancy libraries with command:

.. code-block:: bash

    pip3 install humanize phonenumbers


If you use odoo.sh make sure you have ``requirements.txt`` file in your modules top folder containing:

.. code::

    humanize
    phonenumbers
    
So that odoo.sh can install the required dependencies.

If you use python virtualenv make sure you install the requirements there and not system wide.

Odoo version 10 uses python2, so use command ``pip`` instead of ``pip3``.

Get your Registration code
==========================
Go to ``PBX -> Settings -> Billing``, update your instance settings and click ``GET REGISTRATION CODE`` button.

You must receive an email with subject ``[OdooPBX] Registration code`` to the address specified as admin's email with the registration code.

Enter your instance registration code and click ``SUBMIT REGISTRATION`` button.

Make sure your WEB Base URL is correctly set as this is the address where the Asterisk Plus agent and billing accounting connect.

Check this short manual for more information: `Register_your_Odoo_instance <https://scribehow.com/shared/Register_your_Odoo_instance__yczyIZtZQZycdXLSSlp6NQ>`__.

Update your Payment Profile
===========================
In order to start using Asterisk Plus you must enter your billing details by clicking on ``PAYMENT PROFILE`` button.

First specify your address and after that enter your payment source. 

After that click on the ``SUBSCRIBE`` button to create your subscription.

Check this manual for more information: `Updating_Payment_Profile_and_Subscribing_to_a_product <https://scribehow.com/shared/Updating_Payment_Profile_and_Subscribing_to_a_product__3_GiJbTBSLmkCmmr5fy6VQ>`__.

Next you should proceed with :doc:`agent`.