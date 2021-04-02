"""Conference class"""

from rival_regions_wrapper import functions


class Conference():
    """Wrapper class for confernce"""
    def __init__(self, api_wrapper):
        self.api_wrapper = api_wrapper

    def send_message(self, conference_id, message):
        """send conference message"""
        self.api_wrapper.send_conference_message(conference_id, message)
