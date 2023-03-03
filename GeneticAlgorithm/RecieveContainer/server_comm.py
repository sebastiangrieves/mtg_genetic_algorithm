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
    ssh.connect('ec2-18-118-104-233.us-east-2.compute.amazonaws.com', username='ubuntu', pkey=k, timeout=None)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    ssh_stdin.close()
    return_logs = ssh_stdout.read().decode("utf-8")
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
    deck_1 = {'name': 'Deck_1', 'color': 'B, U, W', 'cards': [['Adarkar Wastes ', 'DMU'], ['Adarkar Wastes ', 'DMU'], ['Ao, the Dawn Sky', 'NEO'], ['Ao, the Dawn Sky', 'NEO'], ['Caves of Koilos', 'DMU'], ['Caves of Koilos', 'DMU'], ['Dennick, Pious Apprentice ', 'MID'], ['Dennick, Pious Apprentice ', 'MID'], ['Dennick, Pious Apprentice ', 'MID'], ['Dennick, Pious Apprentice ', 'MID'], ['Deserted Beach', 'MID'], ['Deserted Beach', 'MID'], ['Deserted Beach', 'MID'], ['Destroy Evil', 'DMU'], ['Destroy Evil', 'DMU'], ['Eiganjo, Seat of the Empire', 'NEO'], ['Faerie Vandal', 'J22'], ['Faerie Vandal', 'J22'], ['Faerie Vandal', 'J22'], ['Go for the Throat', 'BRO'], ['Go for the Throat', 'BRO'], ['Island ', 'THB'], ['Kaito Shizuki', 'PLIST'], ['Make Disappear', 'SNC'], ['Make Disappear', 'SNC'], ['Make Disappear', 'SNC'], ['Make Disappear', 'SNC'], ['Otawara, Soaring City', 'NEO'], ['Plains ', 'THB'], ['Plaza of Heroes', 'DMU'], ['Plaza of Heroes', 'DMU'], ['Plaza of Heroes', 'DMU'], ["Raffine's Tower", 'SNC'], ["Raffine's Tower", 'SNC'], ["Raffine's Tower", 'SNC'], ["Raffine's Tower", 'SNC'], ['Raffine, Scheming Seer', 'SNC'], ['Raffine, Scheming Seer', 'SNC'], ['Raffine, Scheming Seer', 'SNC'], ['Raffine, Scheming Seer', 'SNC'], ['Reckoner Bankbuster', 'NEO'], ['Reckoner Bankbuster', 'NEO'], ['Shattered Sanctum', 'VOW'], ['Shattered Sanctum', 'VOW'], ['Shattered Sanctum', 'VOW'], ['Sheoldred, the Apocalypse ', 'ONE'], ['Sheoldred, the Apocalypse ', 'ONE'], ['Sheoldred, the Apocalypse ', 'ONE'], ['Shipwreck Marsh', 'MID'], ['Shipwreck Marsh', 'MID'], ['Shipwreck Marsh', 'MID'], ['Spell Pierce', '2X2'], ['Takenuma, Abandoned Mire', 'NEO'], ['The Wandering Emperor', 'NEO'], ['The Wandering Emperor', 'NEO'], ['The Wandering Emperor', 'NEO'], ['Wedding Announcement', 'VOW'], ['Wedding Announcement', 'VOW'], ['Wedding Announcement', 'VOW'], ['Wedding Announcement', 'VOW']]}
    determined_decks = {'deck_1' : deck_format(deck_1)}
    command = ' curl -d \'{"games": 10,"decks":' + f'["{gen_input_deck}","{determined_decks["deck_1"]}' + '\"]' + '}\'' + f' -H \'Content-Type:application/json\' -X POST "http://localhost:{port}/simulation"'
    return_logs = connect_command(command)
    return_logs = json.loads(return_logs)
    return return_logs


def get_game_info(id, port):
    success = False
    while success == False:
        command = f'docker logs {port}'
        return_logs = connect_command(command)
        output = return_logs.split('\n')
        searchable_output = output[-1000:]
        for line in searchable_output:
            compare = line[-4:].replace(' ', '')
            compare = compare[-4:].replace('\r', '')
            if compare == f'#{id}':
                match_results = connect_command(f'curl http://localhost:{port}/simulation/{id}')
                success = True

    return match_results


if __name__ == '__main__':
    # print(get_game_info(12))
    deck = {'name': 'ab39e955-5075-4dff-b061-c2a210df67fc', 'color': 'B', 'cards': [['Swamp', 'vow'], ['Snow-Covered Swamp', 'khm'], ['Snow-Covered Swamp', 'khm'], ['Parasitic Grasp', 'vow'], ['Dokuchi Silencer', 'neo'], ['Skemfar Avenger', 'khm'], ['Swamp', 'znr'], ['Reckoner Shakedown', 'neo'], ['Shambling Ghast', 'afr'], ['Swamp', 'vow'], ['Scourge of the Skyclaves', 'znr'], ['Swamp', 'snc'], ['Mage Hunter', 'stx'], ['Swamp', 'vow'], ['Soul Shatter', 'znr'], ['Swamp', 'stx'], ['Champion of the Perished', 'mid'], ['Swamp', 'mid'], ['Dusk Mangler', 'snc'], ['Lithoform Blight', 'znr'], ['Morbid Opportunist', 'mid'], ['Swamp', 'snc'], ['Blood Fountain', 'vow'], ['Tenured Inkcaster', 'stx'], ['Essence Infusion', 'stx'], ['Swamp', 'khm'], ["Groom's Finery", 'vow'], ['Swamp', 'afr'], ['Swamp', 'snc'], ['Priest of the Haunted Edge', 'khm'], ['Swamp', 'neo'], ['Whack', 'snc'], ['Soul Shatter', 'znr'], ['Malakir Blood-Priest', 'znr'], ['Bloodtithe Collector', 'mid'], ['Dockside Chef', 'neo'], ['Tenacious Underdog', 'snc'], ['Champion of the Perished', 'mid'], ['Swamp', 'vow'], ['Umbral Juke', 'stx'], ['Nimana Skitter-Sneak', 'znr'], ['Dreadwurm', 'znr'], ['Dreadfeast Demon', 'vow'], ['Swamp', 'neo'], ['Swamp', 'mid'], ['Gift of Fangs', 'vow'], ['Swamp', 'neo'], ['Swamp', 'neo'], ['Swamp', 'afr'], ['Dig Up the Body', 'snc'], ['Gluttonous Guest', 'vow'], ['Shadow Stinger', 'znr'], ['Ray of Enfeeblement', 'afr'], ['Scourge of the Skyclaves', 'znr'], ['Dusk Mangler', 'snc'], ['Soul Transfer', 'neo'], ['Blade of the Oni', 'neo'], ["Tergrid's Shadow", 'khm'], ['Swamp', 'vow'], ['Invoke Despair', 'neo']]}
    print(deck_format(deck))
    return_logs = send_game(deck_format(deck), 'deck_1', 8000)
    print(return_logs)
    match_results = get_game_info((return_logs['id']), 8000)
    print(match_results)



