import json
import time
from datetime import datetime
import random as rand
import shutil
import uuid
import pika
import os


def deck_list_color(data, color_1, color_2=''):
    color_list = []
    for card in data:
        color_identity = card['color_identity']
        if color_identity == [color_1] or color_identity == [color_1, color_2] or color_identity == [color_2]:
            if 'Land' not in card['type_line'] and 'A-' not in card['name']:
                color_list.append(card)

    return color_list


def search_card(data, name):
    for card in data:
        card_name = card['name']
        if card_name == name:
            return card


def search_lands(data, color):
    land_list = []
    for card in data:
        type_line = card['type_line']
        if 'Land' in type_line:
            if [color] == card['color_identity']:
                land_list.append(card)
    return land_list


def random_card(data):
    x = len(data)
    card_index = rand.randrange(1, x)
    card = data[card_index]
    minimal_card = [card["name"], card['set']]
    return minimal_card


def deck_create(data, color):
    cards = []
    deck = {'name': str(uuid.uuid4()), 'color': color}
    source_lands = search_lands(data, color)
    source_cards = deck_list_color(data, color)
    for i in range(0, 60):
        x = rand.randint(1, 60)
        if x <= 20:
            # add land
            cards.append(random_card(source_lands))
        else:
            # add non land
            added_card = random_card(source_cards)
            if cards.count(added_card) < 4:
                cards.append(added_card)
            else:
                i -= 1
    deck['cards'] = cards

    return deck


def crossover(father, mother):
    # child = [father[:30], mother[30:]]  # first half of father, last half of mother
    child_1 = []
    child_2 = []

    add_card_to_deck(father[:30], child_1)
    add_card_to_deck(mother[30:], child_1)

    add_card_to_deck(father[30:], child_2)
    add_card_to_deck(mother[:30], child_2)

    # make this return a list of 2 dictionaries
    return child_1, child_2


# useless remove
def add_card_to_deck(deck, output_deck):
    for card in deck:
        output_deck.append(card)
    return output_deck


def deck_to_dck(deck, name):
    card_dictionary = {}
    for card in deck:
        card_name = card['name']
        card_set = card['set']
        card_key = '{}|{}'.format(card_name, card_set)
        if card_key not in card_dictionary:
            card_dictionary[card_key] = [0, card_name, card_set]
        card_dictionary[card_key][0] = card_dictionary[card_key][0] + 1

    with open('Decks/deck.txt', 'w') as f:
        f.write(f'[metadata]\nname={name}\n[Avatar]\n\n[Main]\n')
        for key in card_dictionary:
            card = card_dictionary[key]
            f.write('{} {}\n'.format(card[0], card[1]))
        f.write(f'[Sideboard]\n\n[Planes]\n\n[Schemes]\n\n[Conspiracy]\n\n[Dungeon]\n')


def front_side_card(card):
    return_card = card.replace(',', '').removeprefix("A-").replace('\\', '').replace('\'', '')
    position_in = 0
    for letter in return_card:
        if letter == '/':
            return_card = return_card[:position_in]
            break
        position_in += 1
    return return_card


def save_deck(deck, generation=0):
    if generation == 0:
        filename = 'Decks/' + deck['name'] + '.json'
        with open(filename, 'w') as f:
           f.write(json.dumps(deck))
    else:
        try:
            os.makedirs(f'Decks/gen{generation}/')
            filename = f'Decks/gen{generation}/' + deck['name'] + '.json'
            file = open(filename, 'w')
            file.write(json.dumps(deck))
            file.close()
        except:
            filename = f'Decks/gen{generation}/' + deck['name'] + '.json'
            file = open(filename, 'w')
            file.write(json.dumps(deck))
            file.close()


def send_message(deck_1):
    message = {'deck_1': deck_1}
    message_string = json.dumps(message)
    channel.basic_publish(
        exchange='',
        routing_key='games',
        body=message_string,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))


def open_deck_file(name, generation):
    with open(f'Decks/gen{generation}/' + str(name) + '.json') as f:
        deck_1 = json.load(f)
    return deck_1


def mutation(deck, data):
    mutation_coeffecient = 0.05
    colors = deck['color']
    cards = deck['cards']
    new_cards = deck_list_color(data, colors[0][0], colors[1][0] if len(colors) == 2 else '')
    for i in range (1, rand.randint(0, int(mutation_coeffecient*100))):
        cards[rand.randrange(0, len(cards))] = random_card(new_cards)
        print(i)
    deck['cards'] = cards
    return deck


def deck_color(cards):
    colors = []
    with open('standard_card_list.json') as f:
        data = json.load(f)
    for card in cards:
        card_name = card[0]
        card = search_card(data, card_name)
        if not colors.__contains__(card['colors']):
            if card['colors']:
                colors.append(card['colors'])

    return colors


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='games')
    channel.queue_declare(queue='fitness_queue')
    channel.queue_declare(queue='log_queue')

    #os.makedirs('Decks/')
    with open('standard_card_list.json') as f:
        data = json.load(f)
#    mutation(deck_create(data, 'B'))
    for i in range(30):
        deck_1 = deck_create(data, 'B')
        save_deck(deck_1)
        send_message(deck_1)

        #text color black
        #

