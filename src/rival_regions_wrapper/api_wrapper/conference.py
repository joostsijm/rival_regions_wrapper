"""Conference class"""

import time

from rival_regions_wrapper import authentication_handler, LOGGER
from rival_regions_wrapper.api_wrapper.abstract_wrapper import AbstractWrapper


class Conference(AbstractWrapper):
    """Wrapper class for confernce"""
    def __init__(self, api_wrapper, conference_id):
        AbstractWrapper.__init__(self, api_wrapper)
        self.conference_id = conference_id

    @authentication_handler.session_handler
    def message(self, message):
        """Send message to conference"""
        LOGGER.info(
                '"%s": CONF "%s": start send message',
                self.api_wrapper.client.username, self.conference_id
            )
        browser = self.api_wrapper.client.get_browser()
        try:
            browser.go_to(
                    'https://rivalregions.com/#slide/conference/{}'
                    .format(self.conference_id)
                )
            browser.refresh()
            time.sleep(2)

            character_count = 0
            tmp_messages = []
            for sentence in message.split('\n'):
                sentence_character_count = 0
                tmp_sentence = []
                for word in sentence.split(' '):
                    sentence_character_count += len(word) + 1
                    if sentence_character_count >= 899:
                        message = '{}\n{}'.format('\n'.join(
                                tmp_messages),
                                ' '.join(tmp_sentence)
                            )
                        LOGGER.info(
                                '"%s": CONF "%s": next message length: %s',
                                self.api_wrapper.client.username,
                                self.conference_id, len(message)
                            )
                        browser.type(message, id='message')
                        browser.click(id='chat_send')
                        sentence_character_count = 0
                        tmp_sentence = []
                        character_count = 0
                        tmp_messages = []
                    tmp_sentence.append(word)

                sentence = ' '.join(tmp_sentence)
                character_count += len(sentence) + 1
                if character_count >= 900:
                    message = '\n'.join(tmp_messages)
                    LOGGER.info(
                            '"%s": CONF "%s": next message length: %s',
                            self.api_wrapper.client.username,
                            self.conference_id, len(message)
                        )
                    browser.type(message, id='message')
                    browser.click(id='chat_send')
                    character_count = 0
                    tmp_messages = []
                tmp_messages.append(sentence)

            if tmp_messages:
                message = '\n'.join(tmp_messages)
                LOGGER.info(
                        '"%s": CONF "%s": next message length: %s',
                        self.api_wrapper.client.username,
                        self.conference_id, len(message)
                    )
                browser.type(message, id='message')
                browser.click(id='chat_send')

            LOGGER.info(
                    '"%s": CONF "%s": finished sending message',
                    self.api_wrapper.client.username, self.conference_id
                )
        finally:
            browser.close_current_tab()

    @authentication_handler.session_handler
    def notification(self, message, sound):
        """Send notification to conference"""
        LOGGER.info(
                '"%s": CONF: %s notification',
                self.api_wrapper.client.username, self.conference_id
            )
        data = {
            'sound': 1 if sound else 0,
            'text': message,
            'c': self.api_wrapper.client.var_c,
        }

        if self.api_wrapper.client.session:
            response = self.api_wrapper.client.session.post(
                "https://rivalregions.com/rival/konffcm/{}/".format(
                    self.conference_id
                ),
                data=data
            )
            self.api_wrapper.client.check_response(response)
        else:
            raise authentication_handler.NoLogginException()
        LOGGER.info(
                '"%s": CONF: id %s send notification ',
                self.api_wrapper.client.username, self.conference_id
            )
        return response.text

    @authentication_handler.session_handler
    def change_title(self, title):
        """Change title of conference"""
        LOGGER.info(
                '"%s": CONF: %s change title: %s',
                self.api_wrapper.client.username, self.conference_id, title
            )
        data = {
            't': title,
            'c': self.api_wrapper.client.var_c,
        }

        if self.api_wrapper.client.session:
            response = self.api_wrapper.client.session.post(
                "https://rivalregions.com/rival/changename/{}/".format(
                    self.conference_id
                ),
                data=data
            )
            self.api_wrapper.client.check_response(response)
        else:
            raise authentication_handler.NoLogginException()
        LOGGER.info(
                '"%s": CONF: id %s changed title',
                self.api_wrapper.client.username, self.conference_id
            )
        return response.text
