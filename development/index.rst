----------------------------
Developer Guide Introduction
----------------------------
Introduction
------------
OdooPBX platform stands on **three** whales:
 
* Odoo
* `Nameko microservices framework <https://nameko.io>`__
* Asterisk

There is no direct connection between Odoo & Asterisk. A special **middleware** process is in between
that we call the **Agent middleware**. So it is a **full Asterisk connector** based on Nameko platform.

The Agent middleware is usually run on the same server with Asterisk and it connects to the Asterisk Manager Interface (AMI)
and forwards AMI messages to Odoo.

The **AMI Events** that are sent to Odoo by the agent are **configured** in Asterisk Plus settings.
So the only one requirement that needs to be done in order to start handling AMI events in Odoo is an **XML data** where
it is defined.

Odoo sends jobs to the Agent which in turn submits them to connected Asterisk.

This is non-blocking process. So Odoo worker does not wait for any reply from the Asterisk. And this
is a very important pattern as Odoo cannot be affected by Asterisk outages. 
When something wrong happens with the connection with Asterisk Odoo just works as normal.

When a job it is executed and the result is sent to Odoo using JSON-RPC so as the Agent has a direct
JSON-RPC connection to Odoo and sends the job result *directly*.

The most often job that is called from Odoo is ``asterisk.manager_action`` with an 
`Action <https://wiki.asterisk.org/wiki/display/AST/Asterisk+16+AMI+Actions>`__ as a parameter.

And the most often AMI action is ``Originate``. Here is an example of a click-to-call button:

.. code:: python

    action = {
        'Action': 'Originate',
        'Context': 'from-internal',
        'Priority': '1',
        'Timeout': 60000,
        'Channel': 'SIP/101',
        'Exten': '100',
        'Async': 'true',
    }
    server.local_job('asterisk.manager_action', action)

This is how Odoo creates (originates) a call in Asterisk.

Now check more then `158 Asterisk Actions <https://wiki.asterisk.org/wiki/display/AST/Asterisk+16+AMI+Actions>`__ 
and get the idea what can be integrated in your Odoo with few lines of code.

Here is a new snippet:

.. code:: python

    def originate(self, number, trunk, exten, context)

    action = {
        'Action': 'Originate',
        'Context': context,
        'Priority': '1',
        'Timeout': 60000,
        'Channel': '{}/{}'.format(trunk, number),
        'Exten': exten,
        'Async': 'true',
    }
    server.local_job(
        'asterisk.manager_action',
        action,
        res_model='asterisk_plus.server',
        res_method='originate_call_response'
        pass_back={'uid': self.env.uid},
    )

    @api.model
    def originate_call_response(self, data, pass_back):
        debug(self, 'Originate', data)
        if data[0]['Response'] == 'Error':
            self.env.user.asterisk_plus_notify(
                data[0]['Message'], uid=pass_back['uid'], warning=True)

You should pay attention at ``res_model`` and ``res_method`` parameters of ``local_job`` function.

When AMI Originate fails it returns a response with an error message. 
This response is delivered out of the ``originate`` function.

This is so called **callbacks pattern**.  You call an action and specify what function will receive 
the result when it's done. 

AMI events
----------
See full list of events `here <https://wiki.asterisk.org/wiki/display/AST/Asterisk+16+AMI+Events>`__.

Just create XML-data files with your desired events and write Odoo code to handle them.

.. code:: XML

    <record id="cdr" model="asterisk_plus.event">
      <field name="name">Cdr</field>
      <field name="source">AMI</field>
      <field name="model">asterisk_calls.call</field>
      <field name="method">create_cdr</field>
    </record>
    
Then just create a method in Odoo:

.. code:: python

    @api.model
    def create_cdr(self, event):
        get =  event.get
        self.create({
            'accountcode': get('AccountCode'),
            'src': get('Source'),
            'dst': get('Destination'),
            'dcontext': get('DestinationContext'),
            'clid': get('CallerID'),
            'channel': get('Channel'),
            'started': get('StartTime') or False,
            'answered': get('AnswerTime') or False,
            'ended': get('EndTime') or False,
            'duration': get('Duration'),
            'billsec': get('BillableSeconds'),
            'disposition': get('Disposition'),
            'uniqueid': get('UniqueID') or get('Uniqueid'),
            'linkedid': get('linkedid'),
            'userfield': get('UserField'),
        })
        return True

That's it. Now you have Asterisk call statistics in Odoo without programming anything outside Odoo.

Asterisk console
----------------
What is fun with OdooPBX is that you have a full featured color console right in your Odoo.

You can enter Asterisk commands there or even enter '!' and exit into Linux shell for deep
debugging like running ``sngrep`` SIP sniffer for example or troubleshooting
RTP with ``tcpdump``.

Conclusion
----------
It was a brief introduction to OdooPBX development. 

Check other developer documentation and have a fantastic experience with OdooPBX platform!
