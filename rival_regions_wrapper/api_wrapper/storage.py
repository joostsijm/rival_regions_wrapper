"""Profile class"""

import re

from bs4 import BeautifulSoup

from . import MIDDLEWARE


class Storage(object):
    """Wrapper class for profile"""

    @staticmethod
    def info():
        """Get profile"""
        path = 'storage'
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')
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
        storage = {}
        for key, item_id in keys.items():
            storage[key] = int(soup.find('span', {'urlbar' : item_id}).text.replace('.', ''))
            storage['{}_max'.format(key)] = int(soup.find('span', {'urlbar' : item_id})['maxstore'])

        print(storage)
        return storage
