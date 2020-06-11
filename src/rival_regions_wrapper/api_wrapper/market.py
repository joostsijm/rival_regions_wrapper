"""Profile class"""

import re

from bs4 import BeautifulSoup


class Market():
    """Wrapper class for profile"""
    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper

    def info(self, resource):
        """Get profile"""
        keys = {
            'oil': 3,
            'ore': 4,
            'uranium': 11,
            'diamonds': 15,
            'liquid_oxygen': 21,
            'helium-3': 24,
            'rivalium': 26,
            'antirad': 13,
            'energy_drink': 17,
            'spacerockets': 20,
            'lss': 25,
            'tanks': 2,
            'aircrafts': 1,
            'missiles': 14,
            'bombers': 16,
            'battleships': 18,
            'laser_drones': 27,
            'moon_tanks': 22,
            'space_stations': 23
        }
        if isinstance(resource, str) and resource in keys:
            resource = keys[resource]
        path = 'storage/listed/{}'.format(resource)
        response = self.api_wrapper.get(path)
        soup = BeautifulSoup(response, 'html.parser')

        offers_tree = soup.find_all(class_='list_link')
        offers = []
        for offer_tree in offers_tree:
            offers.append({
                'player_id': int(
                    re.sub(r'^.*\/', '', offer_tree.select_one('.results_date')['action'])
                ),
                'player_name': offer_tree.select_one('.results_date').string,
                'price': int(float(offer_tree.select('.list_level')[1]['rat'])*100),
                'amount': int(offer_tree.select_one('.list_level.imp.small')['rat']),
            })
        return offers
