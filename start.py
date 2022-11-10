#!/usr/bin/env python
import pika
import sys
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
queue_receive = 'hello_recieve'


channel.queue_declare(queue='hello')
channel.queue_declare(queue='hello_recieve')

message = ' '.join(sys.argv[1:]) or "Hello World!"

# original 300 messages
for x in range(0, 300):
    time.sleep(.1)
    # make this function as well
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(" [x] Sent %r" % message)


def on_message(ch, method, properties, body):
    message = body.decode('UTF-8')
    time.sleep(2)
    print(message)


def main():
    channel.queue_declare(queue=queue_receive)

    channel.basic_consume(queue=queue_receive, on_message_callback=on_message, auto_ack=True)

    print('Subscribed to ' + queue_receive + ', waiting for messages...')
    channel.start_consuming()


if __name__ == '__main__':
    rabbit_host = 'localhost'
    print('The RabbitMQ Host IP is: {}'.format(rabbit_host))
    main()
# add something to recieve from hello_recieve and change it the send back to hello
connection.close()