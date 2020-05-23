"""Profile class"""

import re

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
