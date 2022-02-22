===========
Quick Start
===========

This guide will help you to setup everything running inside Docker containers.
So install docker and docker-compose, refer to  `oficial documentation <https://docs.docker.com/engine/install/>`_ for help.

.. important::
   Minimum 2GB RAM is required

Create odoopbx directory, put inside docker-compose.yml from https://github.com/odoopbx/agent and run docker-compose:

.. code:: bash

    mkdir odoopbx
    cd odoopbx
    wget https://raw.githubusercontent.com/odoopbx/agent/master/docker/docker-compose.yml
    docker-compose up -d odoo asterisk agent

You may check with ``docker-commpose ps`` if everything is ok.

Odoo listens at port ``8072`` by default.
Point your browser to http://your.server.address:8072 and enter admin/admin as username/password.

Navigate to ``Apps`` menu in the top-left and search for ``asterisk`` in the search-box.
Choose ``Asterisk Plus`` and press ``Install`` button.

``Asterisk Plus`` module adds ``PBX`` menu into top-left button.
All our PBX stuff lives here.

Navigate to ``Settings`` -> ``Server``, press ``Minion Ping``, ``Asterisk Ping`` buttons to check connectivity with Agent and Asterisk.
