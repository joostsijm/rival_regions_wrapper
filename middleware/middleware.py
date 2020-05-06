"""middleware class"""

from abc import ABC, abstractmethod

from authentication_handler import AuthenticationHandeler


class MiddlewareBase(ABC):
    """Middleware abstract base class"""

    @abstractmethod
    def get(self, path, add_c_var=False):
        """Send get request"""

    @abstractmethod
    def post(self, path, data=None):
        """Send post request"""


class LocalAuthentication(MiddlewareBase):
    """Local authentication"""

    def __init__(self, username, password, login_method):
        self.username = username
        self.password = password
        self.login_method = login_method
        super().__init__()

    def get(self, path, add_c_var=False):
        """Send get requests"""

    def post(self, path, data=None):
        """Send post request"""


class RemoteAuthentication(MiddlewareBase):
    """Remote authentication"""

    def __init__(self, api_url, authentication_key):
        self.api_url = api_url
        self.authentication_key = authentication_key
        super().__init__()

    def get(self, path, add_c_var=False):
        """Send get requests"""

    def post(self, path, data=None):
        """Send post request"""
