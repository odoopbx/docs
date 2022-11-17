
==========
Demo setup
==========
This guide will help you to setup everything running inside Docker containers.
So install docker and docker-compose, refer to  `oficial documentation <https://docs.docker.com/engine/install/>`_ for help.

.. important::
   Minimum 2GB RAM is required

Steps to setup a new project:

*  `Get docker-compose.yml <https://github.com/odoopbx/agent/blob/master/docker/docker-compose.yml>`__.
*  Run it.

Commands to copy & run:

.. code:: bash

    mkdir /srv/odoopbx
    cd /srv/odoopbx
    wget https://raw.githubusercontent.com/odoopbx/agent/master/docker/docker-compose.yml
    docker-compose up -d odoo pbx

You may check with ``docker-commpose ps`` if everything is ok.

Odoo listens at port ``8072`` by default.
Point your browser to http://your.server.address:8072 and enter admin/admin as username/password.

Navigate to ``Apps`` menu in the top-left and search for ``asterisk`` in the search-box.
Choose ``Asterisk Plus`` and press ``Install`` button.

``Asterisk Plus`` module adds ``PBX`` menu into top-left button.
All our PBX stuff lives here.

Navigate to ``Settings`` -> ``Server``, press ``Minion Ping``, ``Asterisk Ping`` buttons to check connectivity with Agent and Asterisk.

Enjoy!
