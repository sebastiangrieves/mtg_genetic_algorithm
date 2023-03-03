import pika, json, os, random as rand
import server_comm
import time


#assign ea h container in here to one within the vm
def log_send(results):
    message = results
    channel.basic_publish(
        exchange='',
        routing_key='log_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))


def play_games(deck, port):
    print(deck)
    deck = server_comm.deck_format(deck)
    total_results = {}
    for i in range(5):
        return_logs = server_comm.send_game(deck, 'deck_1', port)
        print((return_logs['id']))
        results = server_comm.get_game_info((return_logs['id']), port)
        total_results[f'game_{i}'] = results
        log_send(results)

    print(total_results)

    # assign each container in here to one within the vm
    # set an environmental variable that increments 8000,8001...

    return total_results


def send_message(deck_and_wins):
    deck_and_wins = json.dumps(deck_and_wins)
    print(deck_and_wins)
    message = deck_and_wins.encode('UTF-8')
    print(message)
    print('Sending Fitness')
    channel.basic_publish(
        exchange='',
        routing_key='fitness_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))


def on_message(ch, method, properties, body):
    print("Taken in deck")
    message = body.decode('UTF-8')
    decks = json.loads(message)
    results = play_games(decks['deck_1'], port)
    send_message(results)
    print(results)


if __name__ == '__main__':
    host = os.environ['RABBIT_HOST']
    queue_receive = os.environ['QUEUE_NAME']
    port = os.environ['PORT']
    connection_params = pika.ConnectionParameters(host=host, blocked_connection_timeout=300)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.basic_consume(queue=queue_receive, on_message_callback=on_message, auto_ack=True)

    print('Subscribed to ' + queue_receive + ', waiting for messages...')
    channel.start_consuming()
    on_message(ch='games')


# play against 5 top
# percentage of wins is fitness score
# play queue
# lowest member if winner is higher kicked
# games per 5
# new deck is bred with all in pool
# deck pool size

