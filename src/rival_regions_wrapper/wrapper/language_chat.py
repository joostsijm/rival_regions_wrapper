"""Language chat class"""

from rival_regions_wrapper import LOGGER, api
from rival_regions_wrapper.wrapper.abstract_wrapper import AbstractWrapper


class LanguageChat(AbstractWrapper):
    """Wrapper class for language chat"""

    def __init__(self, middleware, language):
        AbstractWrapper.__init__(self, middleware)
        self.language = language

    def message(self, message):
        """send message to language chat"""
        LOGGER.info(
            '"%s": CHAT: language %s', self.middleware.username, self.language
        )
        api.language_message(self.middleware, self.language, message)
