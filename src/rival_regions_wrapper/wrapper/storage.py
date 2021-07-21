"""Storage class"""

from bs4 import BeautifulSoup

from rival_regions_wrapper import util

from rival_regions_wrapper.wrapper.abstract_wrapper import AbstractWrapper


class Storage(AbstractWrapper):
    """Wrapper class for storage"""

    def info(self):
        """storage info"""
        path = "storage"
        response = self.middleware.get(path)
        soup = BeautifulSoup(response, "html.parser")
        storage = {}
        for key, item_id in util.ITEM_KEYS.items():
            storage[key] = int(
                soup.find("span", {"urlbar": item_id}).text.replace(".", "")
            )
            storage["{}_max".format(key)] = int(
                soup.find("span", {"urlbar": item_id})["maxstore"]
            )

        return storage
