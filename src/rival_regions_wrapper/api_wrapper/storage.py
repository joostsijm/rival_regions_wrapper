"""Storage class"""

from bs4 import BeautifulSoup

from rival_regions_wrapper import data_structures

from .abstract_wrapper import AbstractWrapper


class Storage(AbstractWrapper):
    """Wrapper class for storage"""
    def info(self):
        """storage info"""
        path = 'storage'
        response = self.api_wrapper.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        storage = {}
        for key, item_id in data_structures.ITEM_KEYS.items():
            storage[key] = int(
                soup.find('span', {'urlbar': item_id}).text.replace('.', '')
            )
            storage['{}_max'.format(key)] = int(
                soup.find('span', {'urlbar': item_id})['maxstore']
            )

        return storage
