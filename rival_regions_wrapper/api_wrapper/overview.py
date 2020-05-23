"""Profile class"""

import re

from bs4 import BeautifulSoup
from dateutil import parser

from . import MIDDLEWARE


class Overview(object):
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

        auto_war = soup.select_one('.war_index_war span.pointer:nth-child(4)')
        if auto_war.has_attr('action'):
            auto_war = soup.select_one('.war_index_war span.pointer:nth-child(4)')['action']
        else:
            auto_war = None
        overview = {
            'perks': {
                'strenght': int(soup.find('div', {'perk': 1, 'class': 'perk_source_2'}).text),
                'education': int(soup.find('div', {'perk': 2, 'class': 'perk_source_2'}).text),
                'endurance': int(soup.find('div', {'perk': 3, 'class': 'perk_source_2'}).text),
                'upgrade_date': parser.parse(date_string),
                'upgrade_perk': upgrade_perk
            },
            'war': {
                'auto_war': auto_war.replace('war/details/', ''),
            }
        }
        return overview

    @staticmethod
    def status():
        """Get current status"""
        path = 'main'
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        profile_url = soup.select_one('#header_my_avatar')['action']
        party_url = soup.select_one('#party_menu_members')['action']
        stats = {
            'profile_id': int(profile_url.replace('slide/profile/', '')),
            'party_id': int(party_url.replace('listed/party/', '')),
            'gold': int(soup.select_one('#g').text.replace('.', '')),
            'money': int(soup.select_one('#m').text.replace('.', '')),
            'level': int(soup.select_one('#exp_level').text),
            'exp': int(soup.select_one('#exp_points').text),
        }
        return stats
