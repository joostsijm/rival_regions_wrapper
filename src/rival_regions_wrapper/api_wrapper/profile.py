"""Profile class"""

import time
import re

from bs4 import BeautifulSoup

from rival_regions_wrapper import authentication_handler, LOGGER
from rival_regions_wrapper.api_wrapper.abstract_wrapper import AbstractWrapper


class Profile(AbstractWrapper):
    """Wrapper class for profile"""
    def __init__(self, api_wrapper, profile_id):
        AbstractWrapper.__init__(self, api_wrapper)
        self.profile_id = profile_id

    def info(self):
        """Get profile"""
        path = 'slide/profile/{}'.format(self.profile_id)
        response = self.api_wrapper.get(path)
        soup = BeautifulSoup(response, 'html.parser')
        level = soup.select_one('div.oil:nth-child(2) > div:nth-child(2)').text
        perks = soup.select('table tr:nth-child(2) span')
        profile = {
            'profile_id': self.profile_id,
            'name': re.sub(r'.*:\s', '', soup.find('h1').text),
            'level': int(re.sub(r'^Level\:\s|\s\(.*\)$', '', level)),
            'level_percentage': int(
                re.sub(r'^Level\:\s(\d+)\s\(|\s\%\)$', '', level)
            ),
            'strenght': int(perks[0].text),
            'education': int(perks[1].text),
            'endurance': int(perks[2].text),
        }
        return profile

    @authentication_handler.session_handler
    def message(self, message):
        """send personal message"""
        LOGGER.info(
                '"%s": PM: user id %s',
                self.api_wrapper.client.username, self.profile_id
            )
        browser = self.api_wrapper.client.get_browser()
        try:
            browser.go_to(
                    'https://rivalregions.com/#messages/{}'
                    .format(self.profile_id)
                )
            browser.refresh()
            time.sleep(2)
            browser.type(message, id='message')
            browser.click(id='chat_send')
            LOGGER.info(
                    '"%s:" PM: user id %s, finished sending message',
                    self.api_wrapper.client.username, self.profile_id
                )
        finally:
            browser.close_current_tab()
