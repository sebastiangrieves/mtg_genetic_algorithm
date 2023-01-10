import shlex
import string
import os
import json
import subprocess
import re


def deck_format(deck_name):
    command = ''
    with open('../../GeneticAlgorithm/Decks/' + deck_name) as f:
        deck = json.load(f)

    # name of the deck
    command = command + f'[metadata]\\nName={deck_name}\\n[Main]\\n'
    # this adds the cards into the deck command
    for card in deck['cards']:
        if card != deck['cards'][59]:
            command = command + str(card[0]).translate(str.maketrans('','',string.punctuation)) + '|' + str(card[1]).upper() + '\\n'
        else:
            command = command + str(card[0]).translate(str.maketrans('', '', string.punctuation)) + '|' + str(card[1]).upper()

    return command


def send_game(gen_input_deck,determined_input_deck, port):
    os.system('curl -d \'{"games": 10,"decks":'+ f'["{gen_input_deck}","{determined_input_deck}' + '\"]' + '}\'' + f' -H \'Content-Type:application/json\' -X POST http://10.30.2.199:{port}/simulation')
    args = shlex.split('curl -d \'{"games": 10,"decks":'+ f'["{gen_input_deck}","{determined_input_deck}' + '\"]' + '}\'' + f' -H \'Content-Type:application/json\' -X POST http://10.30.2.199:{port}/simulation')
    a = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    a = a.decode("utf-8")
    return a

def get_game_info(id, port):
    os.system(f'curl http://10.30.2.199:{port}/simulation/{id}')
    args = shlex.split(f'curl http://10.30.2.199:{port}/simulation/{id}')
    a = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    a = a.decode("utf-8")
    game_json = json.loads(a)
    game_log = game_json['log']
    match_results = game_log[-2].replace(' ', ':').split(':')
    match_results = list(filter(lambda b: b != '', match_results))
    return match_results


if __name__ == '__main__':
    # print(get_game_info(12))
    #print(send_game(deck_format('gen1/0d9824e6-db33-46fc-ae3f-28c62c29144f.json'),deck_format('gen5/0b176a93-8558-48fb-b1e4-065622ee86a4.json'),8000))
    get_game_info(15, 8000)

