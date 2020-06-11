"""Resource state class"""

import re

from bs4 import BeautifulSoup


class ResourceState():
    """Wrapper class for resource state"""
    def __init__(self, api_wrapper, state_id):
        self.api_wrapper = api_wrapper
        self.state_id = state_id

    def info(self, resource):
        """Get resource state"""
        keys = {
            3: 'oil',
            4: 'ore',
            11: 'uranium',
            15: 'diamonds'
        }
        if isinstance(resource, int) and resource in keys:
            resource = keys[resource]
        path = 'listed/stateresources/{}/{}'.format(self.state_id, resource)
        response = self.api_wrapper.get(path)
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
