import server_comm
import GeneticAlgorithm.deck as deck
import json
import os
import subprocess
import re
import paramiko


def format():

    final_deck = []
    final_deck_2 = []
    with open('Deck - Esper Midrange (1).txt') as f:
        deck = f.read()
    deck = re.sub("<.*?>", "", deck)
    deck = deck.split("\n")
    for card in deck:
        card = card.split(' ')
        for i in range(0, int(card[0])):
            final_deck.append(card[1:])
    for card in final_deck:
        new_card = [' '.join(card[:-1])]
        new_card.append(card[-1].replace('[', '').replace(']', ''))
        final_deck_2.append(new_card)
    print(final_deck_2)



if __name__ == '__main__':
    command = 'curl http://localhost:8000/simulation/2'
    k = paramiko.RSAKey.from_private_key_file('RealKeyHere.pem')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('ec2-18-118-104-233.us-east-2.compute.amazonaws.com', username='ubuntu', pkey=k, timeout=None)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    ssh_stdin.close()
    print(ssh_stdout.read().decode('UTF-8'))







