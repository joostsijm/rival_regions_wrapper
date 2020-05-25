"""Profile class"""

import re
from datetime import timedelta

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
        # heading = soup.find('h1')
        pattern = re.compile('.war_det_cou')
        pattern = re.compile('.war_det_cou')
        script = soup.find('script', text=pattern)
        search_result = re.search(r'\'\d+\'', str(script))
        if search_result:
            seconds = int(search_result.group(0).replace('\'', ''))
            time_left = timedelta(seconds=seconds)
            time_left = time_left - timedelta(time_left.days)
        war_info = {
            'attack': {
                'damage': int(soup.select_one('.war_w_target_a').text.replace('.', ''))
            },
            'defence': {
                'damage': int(soup.select_one('.war_w_target_d').text.replace('.', ''))
            }
        }
        return war_info
