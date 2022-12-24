=========
Debugging
=========
This guide is sharing some tips, tricks and configuration settings 
that are useful during development or issue solving.

Tracing the Agent middleware
============================
Tracing Nameko bus
------------------
Enter Nameko shell:

.. code:: sh
  
  cd /services
  nameko shell -c config.yml

For example, you can send Ping action to Asterisk:

.. code::

  n.rpc.asterisk.manager_action({'Action':'Ping'})
  

Tracing AMI and Odoo RPC
=========================
See LOGGING section in ``/services/config.yml``. You can activate more or less levels there.

*Note: the LOGGING option cannot be passed in environment value.*


Debug the Odoo code
===================
In your module import ``debug`` method.  When debug is enabled in ``PBX -> Settings -> General`` Odoo will these messages
in a special way that is handy to observe. Here is an example:

.. code:: python

  from .settings import debug
  
  @api.model
  def originate_call_response(self, data, pass_back):
      debug(self, 'Originate', data)

In Odoo you will see the following output:

.. code::

  2021-09-28 13:14:23,123 26449 INFO odoopbx_14 werkzeug: 178.18.34.150 - - [28/Sep/2021 13:14:23] "POST /web/dataset/call_kw/asterisk_plus.server/originate_call HTTP/1.0" 200 - 9 0.003 0.342
  ***** originate_call_response: ORIGINATE: [{'Response': 'Error', 'ActionID': 'action/38073b0b-df2b-43e6-a254-a0b192739339/1/8236', 'Message': 'Extension does not exist.', 'content': ''}]
  2021-09-28 13:14:23,628 26448 INFO odoopbx_14 werkzeug: 127.0.0.1 - - [28/Sep/2021 13:14:23] "POST /jsonrpc HTTP/1.1" 200 - 21 0.009 0.244

Using Vscode IDE
=================
Using the debugger
------------------
With Vscode there is 2 debugging methods:

* Launch Odoo and then attach to it for debug.
* Attach to a running Odoo process and debug it.

There is an issue with launch method because we use Odoo in multiprocessing mode (workers>0).

So in my current setup I use launch method just to start / stop Odoo in multiprocessing mode
and this is a normal development cycle:

* Start Odoo
* Change .py files.
* Restart Odoo.

When it's required to use breakpoints I use second method - attaching to a remote debugger.

In this case before I can attach to a remote debugger I have to start it. To do this I created a 
copy of ``odoo-bin`` called ``odoo-debug`` with the following contents:

.. code:: python

    #!/usr/bin/env python3

    # set server timezone in UTC before time module imported
    __import__('os').environ['TZ'] = 'UTC'
    import odoo
    # Activate a debugger and wait for connection.
    import ptvsd
    ptvsd.enable_attach(address=('192.168.2.1', 5678), redirect_output=True)
    ptvsd.wait_for_attach()

    if __name__ == "__main__":
        odoo.cli.main()

When it's required to start a debug session I stop the first method (launch) and switch to
the second method (attach) and start manually ``odoo-debug`` script in the following manner:

.. code:: python

  python -m ptvsd --host 192.168.2.1 --port 5678 --wait ./odoo-bin -c /etc/odoo/odoo14.conf --dev=xml --workers=0

And then run the attach mode configuration. After debug session is over you have to 
stop manually ``odoo-debug`` and disconnect from the remote debugger in Vscode and switch
back to previous normal work cycly of launch method.

To summarise to start the debug session:

* Stop the current Odoo process launched by Vscode.
* Manually start ``odoo-debug``.
* Debug with breakpoints.
* Disconnect from the debugger.
* Stop ``odoo-debug``.
* Run Odoo with launch method.

After that you can use breakpoints without Odoo restart.

Here is the config file ``launch.json``:

.. code:: json

  {
      "version": "0.2.0",
      "configurations": [
          {
              "name": "Odoo: Debug",
              "type": "python",
              "request": "attach",
              "port": 5678, 
              "host": "192.168.2.1",
              "pathMappings": []
          },
          {
              "name": "Odoo: Run",
              "type":"python",
              "request":"launch",
              "stopOnEntry": false,
              "python":"${command:python.interpreterPath}",
              "console":"integratedTerminal",
              "program":"/srv/odoo/src/odoo-14.0/odoo-bin",
              "args": [
                  "--dev=xml",
                  "--workers=2",
                  "--config=/etc/odoo/odoo14.conf"
              ],
              "cwd":"/srv/odoo/src/odoo-14.0/",
              "gevent": true,
              "env": {},            
              "debugOptions": [
                  "RedirectOutput"
              ]
          },
          {
              "name": "Python: Current File (Integrated Terminal)",
              "type": "python",
              "request": "launch",
              "program": "${file}",
              "console": "integratedTerminal"
          }        
      ]
  }

Here is a short video demonstrating the workflow:

.. youtube:: RcAPFGwZXgw

Increasing file monitor setting
-------------------------------
If you see the following error after Vscode startup:

.. code:: 

  Unable to watch for file changes in this large workspace folder. Please follow the instructions link to resolve this issue.

that means you have to tune your linux pc. Put the following line to ``/etc/sysctl.conf``:  

.. code:: 

  fs.inotify.max_user_watches=524288

And enable it:

.. code:: 
  
  sysctl -w fs.inotify.max_user_watches=524288

*You don't have to enable it after reboot as it's will be activated from the /etc/sysctl.conf.*

