"""Test module"""

import sys
import json

from rival_regions_wrapper import Client


def read_credentials(filename):
    """Read credentials from filename"""
    with open(filename) as credential_file:
        return json.load(credential_file)

def login(credentials=None):
    """Main method"""
    if credentials is None:
        credentials = {}
        credentials['username'] = input("Username: ")
        credentials['password'] = input("Password: ")
        credentials['method'] = input("Login Method: ")

    client = Client(show_window=True)
    client.login(credentials)
    print(client.var_c)

    action_dict = {
        'market': market,
        'oil_market': oil_market,
        'article': article,
        'get': get,
        'gold_exploration': gold_exploration,
        'vote_law': vote_law,
    }
    print(action_dict.keys())
    while True:
        action = input("Action: ")
        if action in action_dict:
            action_dict[action](client)
        else:
            print('action not found')

def market(client):
    """Get all market prices"""
    market_info = client.get_all_market_info()
    for i in market_info:
        print("")
        print(i.upper())
        print("#"*len(i))
        for j in market_info[i]:
            print(j.upper() + ':' + market_info[i][j])

def oil_market(client):
    """Get oil market price"""
    print(client.market_info('oil'))

def article(client):
    """Create article"""
    client.create_article('Nothing to see here', '')

def get(client):
    """Send get request from client"""
    path = input('Path: ')
    result = client.get(path)
    print(result)

def gold_exploration(client):
    """Create gold exploration law"""
    resoure = 0
    data = {
        'tmp_gov': resoure
    }
    result = client.post('parliament/donew/42/{}/0'.format(resoure), data)
    print(result)

def vote_law(client):
    """Vote for a law"""
    # p400220003260451563564814
    # p4002 2000326045 1563564814
    # 'parliament/votelaw/4002/2000326045/1563564814/pro'
    # 'parliament/votelaw/4002/2000326045/1563565114/pro'
    region_id = 4002
    player_id = 2000326045
    law_id = 1563565114
    result = client.post('parliament/votelaw/{}/{}/{}/pro'.format(
        region_id,
        player_id,
        law_id
    ), {})
    print(result)
    

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        CREDENTIALS = read_credentials(sys.argv[1])
        login(CREDENTIALS)
    else:
        login()
