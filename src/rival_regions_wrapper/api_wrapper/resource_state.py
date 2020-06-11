"""Profile class"""

import re

from bs4 import BeautifulSoup

from . import MIDDLEWARE


class ResourceState(object):
    """Wrapper class for profile"""

    @staticmethod
    def info(state_id, resource):
        """Get profile"""
        keys = {
            3: 'oil',
            4: 'ore',
            11: 'uranium',
            15: 'diamonds'
        }
        if isinstance(resource, int) and resource in keys:
            resource = keys[resource]
        path = 'listed/stateresources/{}/{}'.format(state_id, resource)
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        regions_tree = soup.find_all(class_='list_link')
        regions = []
        for region_tree in regions_tree:
            columns = region_tree.find_all('td')
            regions.append({
                'region_id': int(region_tree['user']),
                'region_name': re.sub('Factories: .*$', '', columns[1].text),
                'explored': float(columns[2].string),
                'maximum': int(float(columns[3].string)),
                'deep_exploration': int(columns[4].string),
                'limit_left': int(columns[5].string),
            })
        return regions
