RabbitMQ administration

# Purge all queues

rabbitmqctl list_queues | awk '{ print $1 }' | xargs -L1 rabbitmqctl purge_queue