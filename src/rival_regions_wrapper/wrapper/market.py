"""Profile class"""

import re

from bs4 import BeautifulSoup

from rival_regions_wrapper import util
from rival_regions_wrapper.wrapper.abstract_wrapper import AbstractWrapper


class Market(AbstractWrapper):
    """Wrapper class for profile"""

    def info(self, resource):
        """Get profile"""
        if isinstance(resource, str) and resource in util.ITEM_KEYS:
            resource = util.ITEM_KEYS[resource]
        path = "storage/listed/{}".format(resource)
        response = self.middleware.get(path)
        soup = BeautifulSoup(response, "html.parser")

        offers_tree = soup.find_all(class_="list_link")
        offers = []
        for offer_tree in offers_tree:
            offers.append(
                {
                    "player_id": int(
                        re.sub(
                            r"^.*\/",
                            "",
                            offer_tree.select_one(".results_date")["action"],
                        )
                    ),
                    "player_name": offer_tree.select_one(
                        ".results_date"
                    ).string,
                    "price": int(
                        float(offer_tree.select(".list_level")[1]["rat"])
                        * 100
                    ),
                    "amount": int(
                        offer_tree.select_one(".list_level.imp.small")["rat"]
                    ),
                }
            )
        return offers
