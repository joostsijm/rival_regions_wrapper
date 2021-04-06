"""Language chat class"""

import time

from rival_regions_wrapper import authentication_handler, LOGGER
from rival_regions_wrapper.api_wrapper.abstract_wrapper import AbstractWrapper


class LanguageChat(AbstractWrapper):
    """Wrapper class for language chat"""
    def __init__(self, api_wrapper, language):
        AbstractWrapper.__init__(self, api_wrapper)
        self.language = language

    @authentication_handler.session_handler
    def message(self, message):
        """send message to language chat"""
        LOGGER.info(
                '"%s": CHAT: language %s',
                self.api_wrapper.client.username, self.language
            )
        browser = self.api_wrapper.client.get_browser()
        try:
            browser.go_to(
                    'https://rivalregions.com/#slide/chat/lang_{}'
                    .format(self.language)
                )
            browser.refresh()
            time.sleep(2)
            browser.type(message, id='message')
            browser.click(id='chat_send')
            LOGGER.info(
                    '"%s": CHAT: language %s, finished sending message',
                    self.api_wrapper.client.username, self.language
                )
        finally:
            browser.close_current_tab()
