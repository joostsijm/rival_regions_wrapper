"""Language chat class"""

import time

from rival_regions_wrapper import authentication_handler, LOGGER
from rival_regions_wrapper.browser import Browser
from rival_regions_wrapper.cookie_handler import CookieHandler
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
        if self.api_wrapper.client.session:
            response = self.api_wrapper.client.session.get(
                    "https://rivalregions.com/#overview"
                )
            self.api_wrapper.client.check_response(response)
            browser = Browser(showWindow=self.api_wrapper.client.show_window)
            browser.go_to('https://rivalregions.com/')
            for cookie_name, value in \
                    self.api_wrapper.client.session.cookies.get_dict().items():
                browser.add_cookie(
                        CookieHandler.create_cookie(cookie_name, None, value)
                    )
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
            browser.close_current_tab()
        else:
            raise authentication_handler.NoLogginException()
