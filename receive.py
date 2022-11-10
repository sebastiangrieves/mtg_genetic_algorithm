#!/usr/bin/env python
import pika, os

# connecting to rabbitmq

host = os.environ.get('RABBIT_HOST')
queue_receive = os.environ.get('QUEUE_NAME')
queue_send = os.environ.get('QUEUE_SEND_NAME')
connection_params = pika.ConnectionParameters(host=host)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
publhellos = 0




def send(message):
    channel.basic_publish(
        exchange='',
        routing_key=queue_send,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))


def on_message(ch, method, properties, body):
    message = body.decode('UTF-8')
    global publhellos
    publhellos = publhellos + 1

    # change this to be a function that triggers after doing something
    message = message + str(publhellos)
    print(message)
    send(message)



def main():
    channel.queue_declare(queue=queue_receive)
    channel.queue_declare(queue=queue_send)

    channel.basic_consume(queue=queue_receive, on_message_callback=on_message, auto_ack=True)

    print('Subscribed to ' + queue_receive + ', waiting for messages...')
    channel.start_consuming()


if __name__ == '__main__':
    rabbit_host = os.environ.get('RABBIT_HOST')
    print('The RabbitMQ Host IP is: {}'.format(rabbit_host))
    main()
