"""Profile class"""

import re
from datetime import timedelta

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
        perks = soup.select('.perk_source_4')
        upgrade_perk = None
        upgrade_date = None
        for perk in perks:
            date_string = perk.select_one('.small')
            if date_string:
                upgrade_perk = int(perk['perk'])
                date_string = re.sub(r'^.*:\s', '', soup.select_one('.perk_source_4 .small').text)
                if 'tomorrow' in date_string:
                    time = re.search(r'\d\d:\d\d', date_string)
                    upgrade_date = parser.parse(time.group(0)) + timedelta(days=1)
                elif 'today' in date_string:
                    time = re.search(r'\d\d:\d\d', date_string)
                else:
                    upgrade_date = parser.parse(date_string)
                break
        perks = {
            'strenght': int(soup.find('div', {'perk': 1, 'class': 'perk_source_2'}).text),
            'education': int(soup.find('div', {'perk': 2, 'class': 'perk_source_2'}).text),
            'endurance': int(soup.find('div', {'perk': 3, 'class': 'perk_source_2'}).text),
            'upgrade_date': upgrade_date,
            'upgrade_perk': upgrade_perk
        }
        return perks
