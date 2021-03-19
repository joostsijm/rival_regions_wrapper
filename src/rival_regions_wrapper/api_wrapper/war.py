"""War class"""

import re
from datetime import datetime, timedelta
import unicodedata

from bs4 import BeautifulSoup

from rival_regions_wrapper import functions


class War():
    """Wrapper class for war"""
    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper

    def page(self):
        """Get training war"""
        path = 'war'
        response = self.api_wrapper.get(path)
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

    def info(self, war_id):
        """Get war info"""
        path = 'war/details/{}'.format(war_id)
        response = self.api_wrapper.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        war_info = {
            'war_id': war_id,
            'damage': int(
                soup.select_one('.war_w_target_o').text.replace('.', '')
            ),
            'attack_hourly_available': bool(soup.select_one('.hide_once_war')),
        }
        heading = soup.find('h1')
        energ_drinks = re.search(r'\d+$', heading.select_one('.small').text)
        if energ_drinks:
            war_info['energ_drinks'] = int(energ_drinks.group(0))

        war_info['type'] = re.sub(r'(,|▶).*', '', heading.text).strip().lower()
        war_type = soup.select_one('.no_pointer')
        if war_type and war_type.text == 'Revolution powers':
            war_info['type'] = 'revolution'

        max_hero = heading.select_one('.max_hero')
        if max_hero is not None:
            war_info['max_hero_name'] = max_hero.text
            war_info['max_hero_id'] = \
                max_hero['action'].replace('slide/profile/', '')

        max_hero_damage_str = ''.join(heading.find_all(
                text=True, recursive=False
            )).strip()
        max_hero_damage = re.search(r'(\d|\.)+', max_hero_damage_str)
        if max_hero_damage:
            war_info['max_hero_damage'] = \
                int(max_hero_damage.group(0).replace('.', ''))

        script = soup.find('script', text=re.compile('.war_det_cou'))
        search_result = re.search(r'\'\d+\'', str(script))
        if search_result:
            seconds = int(search_result.group(0).replace('\'', ''))
            war_info['time_left'] = timedelta(seconds=seconds)
            war_info['finish_date'] = datetime.utcnow() + war_info['time_left']
        else:
            war_info['time_left'] = None
            results = re.search(
                    r'(?<=: ).*',
                    soup.select_one('.slide_title .small').text
                )
            if results:
                war_info['finish_date'] = \
                    functions.parse_date(results.group(0))

        war_info['war_units'] = {}
        for war_unit in soup.select('.war_w_unit_div'):
            war_info['war_units'][war_unit['url']] = war_unit.text

        attack_side = soup.select('#war_w_ata_s .hov2')
        if len(attack_side) >= 3:
            war_info['attack'] = {
                'state_id': int(attack_side[0]['action'].replace(
                    'map/state_details/', '')
                ),
                'state_name': unicodedata.normalize(
                    'NFKD', attack_side[0].text
                ),
                'region_id': int(attack_side[1]['action'].replace(
                    'map/details/', ''
                )),
                'region_name': unicodedata.normalize(
                    'NFKD', attack_side[1].text
                ),
                'damage': int(soup.select_one('.war_w_target_a').text.replace(
                    '.', '')
                ),
            }
        else:
            war_info['attack'] = {
                'damage': int(soup.select_one('.war_w_target_a').text.replace(
                    '.', '')
                ),
            }

        defend_side = soup.select('#war_w_def_s .hov2')
        if len(defend_side) >= 3:
            war_info['defend'] = {
                'state_id': int(defend_side[0]['action'].replace(
                    'map/state_details/', '')
                ),
                'state_name': unicodedata.normalize(
                    'NFKD', defend_side[0].text
                ),
                'region_id': int(defend_side[1]['action'].replace(
                    'map/details/', '')
                ),
                'region_name': unicodedata.normalize(
                    'NFKD', defend_side[1].text
                ),
                'damage': int(soup.select_one('.war_w_target_d').text.replace(
                    '.', ''
                )),
            }
        else:
            war_info['defend'] = {
                'damage': int(soup.select_one('.war_w_target_d').text.replace(
                    '.', ''
                )),
            }

        return war_info
