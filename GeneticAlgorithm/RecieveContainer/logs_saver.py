import pika, json, uuid


def on_message(ch, method, properties, body):
    message = body.decode('UTF-8')
    log = json.loads(message)

    with open(f'Logs/{uuid.uuid4()}', 'w') as f:
        f.write(json.dumps(log))
    print(log)

if __name__ == '__main__':
    connection_params = pika.ConnectionParameters(host='172.20.10.2')
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.basic_consume(queue='log_queue', on_message_callback=on_message, auto_ack=True)

    print('Subscribed to ' + 'log_queue' + ', waiting for messages...')
    channel.start_consuming()
    on_message(ch='log_queue')