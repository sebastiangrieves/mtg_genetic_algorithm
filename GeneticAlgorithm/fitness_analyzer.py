import pika
import json
import uuid
import deck
import time
import datetime


def breed(new_deck, deck_pool):
    with open('Decks/' + str(new_deck['name']) + '.json') as f:
        deck_1 = json.load(f)
    for decks in deck_pool:
        with open('Decks/' + decks + '.json') as f:
            deck_2 = json.load(f)
        children = deck.crossover(deck_1['cards'], deck_2['cards'])
        for child in children:
            added_deck = {'name': str(uuid.uuid4()), 'color': '', 'cards': child}
            deck.save_deck(added_deck)
            deck.send_message(added_deck)


def compare(deck):
    if len(deck_pool) < DECK_POOL_SIZE:
        deck_pool[deck['name']] = deck
    else:
        for deck_from_pool in deck_pool:
            deck_from_pool = deck_pool[deck_from_pool]
            deck_games_won = int(deck['games_won'])
            if deck_games_won > int(deck_from_pool['games_won']):
                worst_deck = min(deck_pool, key=lambda x: deck_pool[x]['games_won'])
                deck_pool.pop(worst_deck)
                breed(deck, deck_pool)
                deck_pool[deck['name']] = deck
                print('Adding stronger deck {}'.format(deck_games_won))
                break


def on_message(ch, method, properties, body):
    # print('{} Received message'.format(datetime.datetime.now()))
    message = body.decode('UTF-8')
    deck = json.loads(message)
    compare(deck)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', heartbeat=600, blocked_connection_timeout=300))
    channel = connection.channel()
    queue_receive = 'fitness_queue'

    deck_pool = {}
    DECK_POOL_SIZE = 8
    i = 0

    channel.basic_consume(queue=queue_receive, on_message_callback=on_message, auto_ack=True)
    channel.start_consuming()
    print('Consuming...')
