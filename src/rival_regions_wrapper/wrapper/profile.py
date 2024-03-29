"""Profile class"""

import re

from bs4 import BeautifulSoup

from rival_regions_wrapper import LOGGER, api
from rival_regions_wrapper.wrapper.abstract_wrapper import AbstractWrapper


class Profile(AbstractWrapper):
    """Wrapper class for profile"""

    def __init__(self, middleware, profile_id):
        AbstractWrapper.__init__(self, middleware)
        self.profile_id = profile_id

    def info(self):
        """Get profile"""
        path = "slide/profile/{}".format(self.profile_id)
        response = self.middleware.get(path)
        soup = BeautifulSoup(response, "html.parser")
        level = soup.select_one(
            "div.oil:nth-child(2) > div:nth-child(2)"
        ).text
        perks = soup.select("table tr:nth-child(2) span")
        profile = {
            "profile_id": self.profile_id,
            "name": re.sub(r".*:\s", "", soup.find("h1").text),
            "level": int(re.sub(r"^Level\:\s|\s\(.*\)$", "", level)),
            "level_percentage": int(
                re.sub(r"^Level\:\s(\d+)\s\(|\s\%\)$", "", level)
            ),
            "strenght": int(perks[0].text),
            "education": int(perks[1].text),
            "endurance": int(perks[2].text),
        }
        return profile

    def message(self, message):
        """send personal message"""
        LOGGER.info(
            '"%s": PM: user id %s', self.middleware.username, self.profile_id
        )
        api.profile_message(self.middleware, self.profile_id, message)
