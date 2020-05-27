"""Profile class"""

import re

from bs4 import BeautifulSoup

from . import MIDDLEWARE


class Work(object):
    """Wrapper class for profile"""

    @staticmethod
    def page():
        """Get work page"""
        path = 'work'
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        factory_header = soup.select_one('.factory_slide')
        work_page = {
            'factory_id': int(factory_header['action'].replace('factory/index/', '')),
            'factory_name': factory_header.text
        }
        factory = soup.select_one('.work_item:nth-child(4)')
        print('"{}"'.format(factory.text))
        return work_page
