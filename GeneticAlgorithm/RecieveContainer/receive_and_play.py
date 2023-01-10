import pika, json, os, random as rand


#assign ea h container in here to one within the vm

def play_games(deck):
    # assign each container in here to one within the vm
    # set an environmental variable that increments 8000,8001...
    games_won = 0
    # in the sim you can put in amount of games you would just ping a message with the amount of games here it randrange
    # deck1
    games_won += rand.randint(0, 21)
    # deck2
    games_won += rand.randint(0, 21)
    # deck3
    games_won += rand.randint(0, 21)
    # deck4
    games_won += rand.randint(0, 21)
    # deck5
    games_won += rand.randint(0, 21)
    result = {'name': deck['name'], 'games_won': games_won}

    return result


def send_message(deck_and_wins):
    message = deck_and_wins
    channel.basic_publish(
        exchange='',
        routing_key='fitness_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))


def on_message(ch, method, properties, body):
    message = body.decode('UTF-8')
    decks = json.loads(message)
    results = json.dumps(play_games(decks['deck_1']))
    send_message(results)
    print(results)


if __name__ == '__main__':
    host = os.environ['RABBIT_HOST']
    queue_receive = os.environ['QUEUE_NAME']
    connection_params = pika.ConnectionParameters(host=host)
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

