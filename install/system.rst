===================
System requirements
===================
OdooPBX is based mainly on Python 3. So it must be properly installed.

On different systems same packages have different names.

We support the most popular Linux distributions.

If something does not work for you it's ok to send us ``cat /etc/*release | mail reports@odoopbx.com`` so 
that we could add support to your system.


Ubuntu and Debian
=================

.. code::

    apt update && apt -y install python3-pip python3-setproctitle
    pip3 install odoopbx

CentOS Versions 6&7
===================
First, you should enable and install Python3 and pip.

There are at least `3 ways to install the latest Python3 package on CentOS <https://www.2daygeek.com/install-python-3-on-centos-6/>`_. 

Below is one of them (IUS).

.. code:: 

    curl 'https://setup.ius.io/' -o setup-ius.sh
    sh setup-ius.sh
    yum --enablerepo=ius install python36 python36-pip python36-setproctitle
    pip3 install odoopbx

.. warning::

   Please note that if you are using FreePBX, which is based on Centos 7, it has a different Python3 naming schema,
   similar to ius, but using Sangoma's own repositories. You shouldn't try to use 3rd party repositories,
   simply run ``yum makecache`` to get latest information from Sangoma's repositories and install Python3 by running 
   ``yum install python36u python36u-pip``

CentOS Version 8
================
Latest CentOS is quite ready for Python3. So here are the installation steps:

.. code::

    yum install python3 python3-pip python3-devel
    pip3 install odoopbx


Sangoma Linux release 7.8
=========================

.. code::

    yum install python36u python36u-pip python36u-devel
    pip3.6 install odoopbx
    

Next - :doc:`standard` or :doc:`docker`.