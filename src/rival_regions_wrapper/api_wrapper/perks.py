"""Perks class"""

import re

from bs4 import BeautifulSoup

from rival_regions_wrapper import functions


class Perks():
    """Wrapper class for perks"""
    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper

    def info(self):
        """Get perks"""
        path = 'main/content'
        response = self.api_wrapper.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        perks = soup.select('.perk_source_4')
        upgrade_perk = None
        upgrade_date = None
        for perk in perks:
            date_string = perk.select_one('.small')
            if date_string:
                upgrade_perk = int(perk['perk'])
                date_string = re.sub(r'^.*:\s', '', soup.select_one('.perk_source_4 .small').text)
                upgrade_date = functions.parse_date(date_string)
                break
        perks = {
            'strenght': int(soup.find('div', {'perk': 1, 'class': 'perk_source_2'}).text),
            'education': int(soup.find('div', {'perk': 2, 'class': 'perk_source_2'}).text),
            'endurance': int(soup.find('div', {'perk': 3, 'class': 'perk_source_2'}).text),
            'upgrade_date': upgrade_date,
            'upgrade_perk': upgrade_perk
        }
        return perks

    def upgrade(self, perk, upgrade_type):
        """Craft item"""
        perk_keys = {
            'strength': 1,
            'education': 2,
            'endurance': 3,
        }
        if isinstance(perk, str) and perk in perk_keys:
            perk_keys = perk_keys[perk]

        upgrade_type_keys = {
            'money': 1,
            'gold': 2,
        }
        if isinstance(upgrade_type, str) and upgrade_type in upgrade_type_keys:
            upgrade_type = upgrade_type_keys[upgrade_type]

        self.api_wrapper.post('perks/up/{}/{}'.format(perk, upgrade_type))
        return True
