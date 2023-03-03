import shlex
import string
import os
import json
import subprocess
import time
import paramiko


def connect_command(command):
    k = paramiko.RSAKey.from_private_key_file('RealKeyHere.pem')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('ec2-3-15-150-193.us-east-2.compute.amazonaws.com', username='ubuntu', pkey=k)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    return_logs = ssh_stdout.read().decode("utf-8")
    ssh_stdin.close()
    return_logs = json.loads(return_logs)
    return return_logs


def deck_format(deck):
    # have this so that it instead can take in the contents of a deck and return the correct format
    command = ''

    # name of the deck
    command = command + f'[metadata]\\nName={deck["name"]}\\n[Main]\\n'
    # this adds the cards into the deck command
    for card in deck['cards']:
        if card != deck['cards'][59]:
            command = command + str(card[0]).translate(str.maketrans('','',string.punctuation)) + '|' + str(card[1]).upper() + '\\n'
        else:
            command = command + str(card[0]).translate(str.maketrans('', '', string.punctuation)) + '|' + str(card[1]).upper()

    return command


def send_game(gen_input_deck,determined_input_deck, port):
    deck_1 = {'name': '23d7b178-da30-4b87-b957-cc74c4a953f8', 'color': 'B', 'cards': [['Takenuma, Abandoned Mire', 'neo'], ['Inscription of Ruin', 'znr'], ['Takenuma, Abandoned Mire', 'neo'], ['Whack', 'snc'], ['Unhallowed Phalanx', 'vow'], ['Infernal Pet', 'khm'], ['Acquisitions Expert', 'znr'], ['Elderfang Disciple', 'khm'], ['Swamp', 'mid'], ['Plumb the Forbidden', 'stx'], ['Vorpal Sword', 'afr'], ['Swamp', 'znr'], ['Swamp', 'neo'], ['Swamp', 'afr'], ["Taborax, Hope's Demise", 'znr'], ['Swamp', 'mid'], ['Incriminate', 'snc'], ['Soul Transfer', 'neo'], ['Shakedown Heavy', 'snc'], ['Jadar, Ghoulcaller of Nephalia', 'mid'], ['Tainted Adversary', 'mid'], ['Swamp', 'snc'], ['Swamp', 'afr'], ['Swamp', 'stx'], ['Cemetery Tampering', 'snc'], ['Mask of Griselbrand', 'mid'], ['Snow-Covered Swamp', 'khm'], ['Swamp', 'stx'], ['Chainflail Centipede', 'neo'], ['Tenacious Underdog', 'snc'], ['Cutthroat Contender', 'snc'], ['Swamp', 'snc'], ['Swamp', 'stx'], ['Gisa, Glorious Resurrector', 'mid'], ['Baleful Mastery', 'stx'], ['Eaten Alive', 'mid'], ['Eradicator Valkyrie', 'khm'], ['Sedgemoor Witch', 'stx'], ['Falkenrath Forebear', 'vow'], ['Gluttonous Guest', 'vow'], ['Bloodline Culling', 'mid'], ['Rot-Tide Gargantua', 'vow'], ["Thieves' Tools", 'afr'], ['Swamp', 'znr'], ['Bloodvial Purveyor', 'vow'], ['Necrosynthesis', 'mid'], ['Karfell Kennel-Master', 'khm'], ['Highborn Vampire', 'znr'], ['Necrosynthesis', 'mid'], ['Unhallowed Phalanx', 'vow'], ['Dreadwurm', 'znr'], ['Rotten Reunion', 'mid'], ['Mukotai Soulripper', 'neo'], ['Body Launderer', 'snc'], ['Manticore', 'afr'], ['Swamp', 'snc'], ['Grim Bounty', 'afr'], ['Shambling Ghast', 'afr'], ['Feign Death', 'afr'], ['Dockside Chef', 'neo']]}
    determined_decks = {'deck_1' : deck_format(deck_1)}
    command = ' curl -d \'{"games": 10,"decks":' + f'["{gen_input_deck}","{determined_decks["deck_1"]}' + '\"]' + '}\'' + f' -H \'Content-Type:application/json\' -X POST "http://localhost:{port}/simulation"'
    return_logs = connect_command(command)
    return return_logs


def get_game_info(id, port):
    command = f'curl http://localhost:8000/simulation/{id}'
    return_logs = connect_command(command)
    print(return_logs)

    while return_logs['success'] == False:
        time.sleep(5)
        return_logs = connect_command(command)
    game_log = return_logs['log']
    match_results = game_log[-2].replace(' ', ':').split(':')
    match_results = list(filter(lambda b: b != '', match_results))
    return match_results


if __name__ == '__main__':
    # print(get_game_info(12))
    deck = {'name': 'ab39e955-5075-4dff-b061-c2a210df67fc', 'color': 'B', 'cards': [['Swamp', 'vow'], ['Snow-Covered Swamp', 'khm'], ['Snow-Covered Swamp', 'khm'], ['Parasitic Grasp', 'vow'], ['Dokuchi Silencer', 'neo'], ['Skemfar Avenger', 'khm'], ['Swamp', 'znr'], ['Reckoner Shakedown', 'neo'], ['Shambling Ghast', 'afr'], ['Swamp', 'vow'], ['Scourge of the Skyclaves', 'znr'], ['Swamp', 'snc'], ['Mage Hunter', 'stx'], ['Swamp', 'vow'], ['Soul Shatter', 'znr'], ['Swamp', 'stx'], ['Champion of the Perished', 'mid'], ['Swamp', 'mid'], ['Dusk Mangler', 'snc'], ['Lithoform Blight', 'znr'], ['Morbid Opportunist', 'mid'], ['Swamp', 'snc'], ['Blood Fountain', 'vow'], ['Tenured Inkcaster', 'stx'], ['Essence Infusion', 'stx'], ['Swamp', 'khm'], ["Groom's Finery", 'vow'], ['Swamp', 'afr'], ['Swamp', 'snc'], ['Priest of the Haunted Edge', 'khm'], ['Swamp', 'neo'], ['Whack', 'snc'], ['Soul Shatter', 'znr'], ['Malakir Blood-Priest', 'znr'], ['Bloodtithe Collector', 'mid'], ['Dockside Chef', 'neo'], ['Tenacious Underdog', 'snc'], ['Champion of the Perished', 'mid'], ['Swamp', 'vow'], ['Umbral Juke', 'stx'], ['Nimana Skitter-Sneak', 'znr'], ['Dreadwurm', 'znr'], ['Dreadfeast Demon', 'vow'], ['Swamp', 'neo'], ['Swamp', 'mid'], ['Gift of Fangs', 'vow'], ['Swamp', 'neo'], ['Swamp', 'neo'], ['Swamp', 'afr'], ['Dig Up the Body', 'snc'], ['Gluttonous Guest', 'vow'], ['Shadow Stinger', 'znr'], ['Ray of Enfeeblement', 'afr'], ['Scourge of the Skyclaves', 'znr'], ['Dusk Mangler', 'snc'], ['Soul Transfer', 'neo'], ['Blade of the Oni', 'neo'], ["Tergrid's Shadow", 'khm'], ['Swamp', 'vow'], ['Invoke Despair', 'neo']]}
    print(deck_format(deck))
    return_logs = send_game(deck_format(deck), 'deck_1', 8000)
    print(return_logs)
    time.sleep(5)
    match_results = get_game_info((return_logs['id']-1), 8000)
    print()



