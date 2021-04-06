"""Conference class"""

from .abstract_wrapper import AbstractWrapper


class Conference(AbstractWrapper):
    """Wrapper class for confernce"""
    def send_message(self, conference_id, message):
        """send conference message"""
        self.api_wrapper.send_conference_message(conference_id, message)
