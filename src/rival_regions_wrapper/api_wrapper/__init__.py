"""API wrapper for Rival Regions"""


from .profile import Profile
from .storage import Storage
from .market import Market
from .resource_state import ResourceState
from .perks import Perks
from .craft import Craft
from .overview import Overview
from .war import War
from .work import Work
from .article import Article


class ApiWrapper:
    """API wrapper"""
    authentication = None

    def __init__(self, authentication):
        """Initialize API wrapper with authentication"""
        self.authentication = authentication

    def get(self, path):
        """Send get requests"""
        return self.authentication.get(path)

    def post(self, path, data=None):
        """Send post request"""
        return self.authentication.post(path, data=data)
