import re

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

def all_results(deck_list):
    total_wins = 0
    for deck in deck_list:
        results = get_results(deck_list[deck])
        total_wins = total_wins + int(results['games_won'])
    send_results = {'name': results['name'], 'games_won': total_wins}
    return send_results
def get_results(deck):
    deck = json.loads(deck)
    match_results = deck['log'][-2:]
    deck_name = match_results[0]
    deck_name = deck_name.split('Ai')
    if 'Deck' in deck_name[1]:
        deck_wins = deck_name[2]
        deck_name = deck_name[2]
    else:
        deck_wins = deck_name[1]
        deck_name = deck_name[1]
    deck_name = re.sub("[\(\[].*?[\)\]]", "", deck_name)
    deck_name = deck_name.split(':')
    deck_name = deck_name[0]
    deck_name = deck_name[1:]

    deck_wins = deck_wins.split(': ')
    deck_wins = deck_wins[len(deck_wins)-1]
    deck_wins = deck_wins.replace(' ', '')
    results = {'name': deck_name, 'games_won': deck_wins}
    return results


def compare(results):
    if len(deck_pool) < DECK_POOL_SIZE:
        deck_pool[results['name']] = results
    else:
        for deck_from_pool in deck_pool:
            deck_from_pool = deck_pool[deck_from_pool]
            deck_games_won = int(results['games_won'])
            if deck_games_won > int(deck_from_pool['games_won']):
                worst_deck = min(deck_pool, key=lambda x: deck_pool[x]['games_won'])
                deck_pool.pop(worst_deck)
                breed(results, deck_pool)
                deck_pool[results['name']] = results
                print('Adding stronger deck {}'.format(deck_games_won))
                break


def on_message(ch, method, properties, body):
    # print('{} Received message'.format(datetime.datetime.now()))
    message = body.decode('UTF-8')
    deck = json.loads(message)
    results = all_results(deck)
    compare(results)


if __name__ == '__main__':
    connection_params = pika.ConnectionParameters(host='172.20.10.2', blocked_connection_timeout=300)
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.basic_consume(queue='fitness_queue', on_message_callback=on_message, auto_ack=True)

    deck_pool = {}
    DECK_POOL_SIZE = 8
    i = 0

    channel.start_consuming()
    print('Consuming...')
