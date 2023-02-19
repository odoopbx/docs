=======================
RabbitMQ administration
=======================

# Purge all queues

.. code::

  rabbitmqctl list_queues | awk '{ print $1 }' | xargs -L1 rabbitmqctl purge_queue