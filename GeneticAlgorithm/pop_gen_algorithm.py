# top half of fitness n stays and breeds, each pair creates 2 children (already have thios crossover method
# save each generation to a folder
# repeat r times

import json
import os
import random as Rand

import deck
from RecieveContainer import receive_and_play
import uuid
import shutil


# create an initial population of n decks
def initial_population(pop_size):
    with open('standard_card_list.json') as f:
        data = json.load(f)
    n = pop_size
    for i in range(n+1):
        deck_intial = deck.deck_create(data, 'B')
        deck.save_deck(deck_intial, 1)


# apply fitness test to each of them, returns the deck name and fitness score
def fitness_for_gen(generation):
    fitness_array_per_deck = []
    for deck in os.listdir(f'Decks/gen{generation}'):
        deck_name = deck
        deck_data = json.load(open(f'Decks/gen{generation}/{deck_name}'))
        deck_fitness = receive_and_play.play_games(deck_data)
        fitness_array_per_deck.append(deck_fitness)
    # contain a tuple with deck name and fitness score

    return fitness_array_per_deck


# mating pool for decks
# returns amount of decks within fitness array(if 48 initial returns 48 new decks
def mating_pool(fitness_array, generation):
    # choose 24 most fit
    length_of_array = len(fitness_array)
    newlist = sorted(fitness_array, key=lambda k: k['games_won'])
    most_twentyfour = fitness_array
    saved_decks = 1
    child_names = []
    for i in range(1, length_of_array//4 + 1):
        children = []
        mother = most_twentyfour.pop(Rand.randint(1, len(most_twentyfour)-1))
        father = most_twentyfour.pop(Rand.randint(1, len(most_twentyfour)-1))

        mother_cards = deck.open_deck_file(mother['name'], generation)
        father_cards = deck.open_deck_file(father['name'], generation)

        children += deck.crossover(mother_cards["cards"], father_cards["cards"])

        deck.save_deck(father_cards, generation + 1)
        deck.save_deck(mother_cards, generation + 1)

        child_names.append(father['name'])
        child_names.append(mother['name'])
        for child in children:
            added_deck = {'name': str(uuid.uuid4()), 'color': '', 'cards': child}
            deck.save_deck(added_deck, generation+1)
            child_names.append(added_deck['name'])
    return child_names


if __name__ == '__main__':
    # initial population has to be a multiple of 8, as we divide by 2 then 4 in mating pool
    # removes Decks and all decks before starting new attempt
    try:
        shutil.rmtree('/Users/sebastiangrieves/PycharmProjects/rabbitmq/GeneticAlgorithm/Decks')
    except:
        print()
    initial_population(48)
    for i in range(1, 10):
        mating_pool(fitness_for_gen(i), i)


#   for results in fitness_array:
#       print(results)
