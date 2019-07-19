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

    action = input("Action: ")
    action_dict = {
        "market": market,
        "oil_market": oil_market,
        "article": article
    }

    if action in action_dict:
        action_dict[action](client)

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
    client.create_article("Test", "Whoops")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        CREDENTIALS = read_credentials(sys.argv[1])
        login(CREDENTIALS)
    else:
        login()
