"""Profile class"""

import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from . import MIDDLEWARE


class War(object):
    """Wrapper class for profile"""

    @staticmethod
    def page():
        """Get training war"""
        path = 'war'
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        pattern = re.compile(r'war\/details\/\d+')
        script = soup.find('script', text=pattern)
        war_url = pattern.search(str(script))
        if war_url:
            training_war = int(war_url.group(0).replace('war/details/', ''))
        else:
            training_war = None
        page = {
            'training_war': training_war
        }
        return page

    @staticmethod
    def info(war_id):
        """Get war info"""
        path = 'war/details/{}'.format(war_id)
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        war_info = {
            'damage': int(soup.select_one('.war_w_target_o').text.replace('.', '')),
            'attack_damage': int(soup.select_one('.war_w_target_a').text.replace('.', '')),
            'defence_damage': int(soup.select_one('.war_w_target_d').text.replace('.', '')),
            'attack_hourly_available': bool(soup.select_one('.hide_once_war')),
        }
        heading = soup.find('h1')
        energ_drinks = re.search(r'\d+$', heading.select_one('.small').text)
        if energ_drinks:
            war_info['energ_drinks'] = int(energ_drinks.group(0))

        header_texts = heading.select('.float_left')
        try:
            war_info['name'] = header_texts[1].text
        except IndexError:
            pass

        max_hero = heading.select_one('.max_hero')
        war_info['max_hero_name'] = max_hero.text
        war_info['max_hero_id'] = max_hero['action'].replace('slide/profile/', '')

        max_hero_damage_str = ''.join(heading.find_all(text=True, recursive=False)).strip()
        max_hero_damage = re.search(r'(\d|\.)+', max_hero_damage_str)
        if max_hero_damage:
            war_info['max_hero_damage'] = int(max_hero_damage.group(0).replace('.', ''))

        script = soup.find('script', text=re.compile('.war_det_cou'))
        search_result = re.search(r'\'\d+\'', str(script))
        if search_result:
            seconds = int(search_result.group(0).replace('\'', ''))
            war_info['time_left'] = timedelta(seconds=seconds)
            war_info['finish_date'] = datetime.now() + war_info['time_left']

        war_info['war_units'] = {}
        for war_unit in soup.select('.war_w_unit_div'):
            war_info['war_units'][war_unit['url']] = war_unit.text
        return war_info
