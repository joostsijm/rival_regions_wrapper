"""Conference class"""

from rival_regions_wrapper import LOGGER, api
from rival_regions_wrapper.wrapper.abstract_wrapper import AbstractWrapper


class Conference(AbstractWrapper):
    """Wrapper class for confernce"""

    def __init__(self, middleware, conference_id):
        AbstractWrapper.__init__(self, middleware)
        self.conference_id = conference_id

    def message(self, message):
        """Send message to conference"""
        LOGGER.info(
            '"%s": CONF "%s": start send message',
            self.middleware.username,
            self.conference_id,
        )
        api.conference_message(self.middleware, self.conference_id, message)

    def notification(self, message, sound):
        """Send notification to conference"""
        LOGGER.info(
            '"%s": CONF: %s notification',
            self.middleware.username,
            self.conference_id,
        )
        return api.conference_notification(
            self.middleware, self.conference_id, message, sound
        )

    def change_title(self, title):
        """Change title of conference"""
        LOGGER.info(
            '"%s": CONF: %s change title: %s',
            self.middleware.username,
            self.conference_id,
            title,
        )
        return api.conference_change_title(
            self.middleware, self.conference_id, title
        )
