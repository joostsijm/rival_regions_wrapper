"""CRAFT class"""

import re

from bs4 import BeautifulSoup


class Craft():
    """Wrapper class for crafting"""
    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper

    def info(self, item):
        """Get craft"""
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
        if isinstance(item, str) and item in keys:
            item = keys[item]
        path = 'storage/produce/{}'.format(item)
        response = self.api_wrapper.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        resources = soup.select_one('.storage_produce_exp')
        resource_dict = {
            'cash': 'white',
            'oil': 'oil',
            'ore': 'ore',
            'uranium': 'uranium',
            'diamond': 'diamond',
            'oxygen': 'oxygen',
        }
        resource_cost = {}
        for name, selector in resource_dict.items():
            element = resources.select_one('.{} .produce_discount'.format(selector))
            if element:
                resource_cost[name] = int(
                    re.sub(r'-|\.', '', element.text)
                )
        craft = {
            'market_price': int(re.sub(r'\.|\s\$', '', soup.select('.small .imp')[1].text)),
            'resources': resource_cost
        }
        return craft

    def produce(self, item, amount):
        """Craft item"""
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
        if isinstance(item, str) and item in keys:
            item = keys[item]
        self.api_wrapper.post('storage/newproduce/{}/{}'.format(item, amount))
        return True
