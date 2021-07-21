"""Profile class"""

from bs4 import BeautifulSoup

from rival_regions_wrapper.wrapper.abstract_wrapper import AbstractWrapper
from rival_regions_wrapper.wrapper.perks import Perks


class Overview(AbstractWrapper):
    """Wrapper class for perks"""

    def info(self):
        """Get overview"""
        path = "main/content"
        response = self.middleware.get(path)
        soup = BeautifulSoup(response, "html.parser")
        perks = Perks.info_parse(soup)
        auto_war = soup.select_one(".war_index_war span.pointer:nth-child(4)")
        if auto_war and auto_war.has_attr("action"):
            auto_war = auto_war["action"].replace("war/details/", "")
        else:
            auto_war = None
        overview = {
            "perks": perks,
            "war": {
                "auto_war": auto_war,
            },
        }
        return overview

    def status(self):
        """Get current status"""
        path = "main"
        response = self.middleware.get(path)
        soup = BeautifulSoup(response, "html.parser")
        profile_url = soup.select_one("#header_my_avatar")["action"]
        party_url = soup.select_one("#party_menu_members")["action"]
        stats = {
            "profile_id": int(profile_url.replace("slide/profile/", "")),
            "party_id": int(party_url.replace("listed/party/", "")),
            "gold": int(soup.select_one("#g").text.replace(".", "")),
            "money": int(soup.select_one("#m").text.replace(".", "")),
            "level": int(soup.select_one("#exp_level").text),
            "exp": int(soup.select_one("#exp_points").text),
        }
        return stats
