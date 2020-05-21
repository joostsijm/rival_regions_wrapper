"""Profile class"""

import re

from bs4 import BeautifulSoup
from dateutil import parser

from . import MIDDLEWARE


class Perks(object):
    """Wrapper class for perks"""

    @staticmethod
    def info():
        """Get perks"""
        path = 'main/content'
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        date_string = re.sub(r'^.*:\s', '', soup.select_one('.perk_source_4 .small').text)
        current_perk = soup.select_one('.perk_source_4:has(.small)')
        if current_perk.has_attr('perk'):
            upgrade_perk = int(current_perk['perk'])
        else:
            upgrade_perk = None
        perks = {
            'strenght': int(soup.find('div', {'perk': 1, 'class': 'perk_source_2'}).text),
            'education': int(soup.find('div', {'perk': 2, 'class': 'perk_source_2'}).text),
            'endurance': int(soup.find('div', {'perk': 3, 'class': 'perk_source_2'}).text),
            'upgrade_date': parser.parse(date_string),
            'upgrade_perk': upgrade_perk
        }
        return perks
