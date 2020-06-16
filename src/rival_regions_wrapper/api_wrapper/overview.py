"""Profile class"""

import re

from bs4 import BeautifulSoup

from rival_regions_wrapper import functions


class Overview():
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
        auto_war = soup.select_one('.war_index_war span.pointer:nth-child(4)')
        if auto_war and auto_war.has_attr('action'):
            auto_war = auto_war['action'].replace('war/details/', '')
        else:
            auto_war = None
        overview = {
            'perks': {
                'strenght': int(soup.find('div', {'perk': 1, 'class': 'perk_source_2'}).text),
                'education': int(soup.find('div', {'perk': 2, 'class': 'perk_source_2'}).text),
                'endurance': int(soup.find('div', {'perk': 3, 'class': 'perk_source_2'}).text),
                'upgrade_date': upgrade_date,
                'upgrade_perk': upgrade_perk
            },
            'war': {
                'auto_war': auto_war,
            }
        }
        return overview

    def status(self):
        """Get current status"""
        path = 'main'
        response = self.api_wrapper.get(path)
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
