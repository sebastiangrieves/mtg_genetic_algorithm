# mtg_genetic_algorithm
Recieve container is everything to do with docker, it has the dockerfile and script to build the image (build.sh).

It also has recieve_and_play.py which is the script that has the decks "play" their games.

Run_crossover.sh is a terminal script that opens 10 containers of the recieve_and_play.py image.

Standard_Card_list is a file with all cards that we are using in our simulation and deck creation.

All_cut_cards are all cards that were supposed to be legal determined by scryfall, but werent usably by forge.

deck.py is the code with everything relating for the deck, and right now creates as many random decks as possible and sending them to the games queue.

fitness_anylazer takes games from the fitness queue and determines if they will remain in the deck pool, if so they are bred with all decks in the deck pool.

Whiteboard sketch is a good visual overview of whats going on.
