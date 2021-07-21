"""middleware class"""

from abc import ABC, abstractmethod

import requests

from rival_regions_wrapper import api
from rival_regions_wrapper.authentication_handler import AuthenticationHandler


class MiddlewareBase(ABC):
    """Middleware abstract base class"""

    username = None

    @abstractmethod
    def get(self, path, add_var_c=False):
        """Send get request"""

    @abstractmethod
    def post(self, path, data=None):
        """Send post request"""


class LocalAuthentication(MiddlewareBase):
    """Local authentication"""

    def __init__(self, show_window=False, captcha_client=None):
        super().__init__()
        self.authentication_handler = AuthenticationHandler(
            show_window, captcha_client
        )

    def set_credentials(self, username, password, login_method):
        """Set login credentials"""
        self.username = username
        self.authentication_handler.set_credentials(
            login_method, username, password
        )
        return self

    def authenticate(self):
        """Authenticate handler"""
        self.authentication_handler.authenticate()

    def get(self, path, add_var_c=False):
        """Send get requests"""
        return api.get(self, path, add_var_c)

    def post(self, path, data=None):
        """Send post request"""
        return api.post(self, path, data=data)


class RemoteAuthentication(MiddlewareBase):
    """Remote authentication"""

    def __init__(self, api_url, authentication_key):
        super().__init__()
        self.api_url = api_url
        self.headers = {"Authorization": authentication_key}

    def get(self, path, add_var_c=False):
        """Send get requests"""
        try:
            response = requests.get(
                "{}{}".format(self.api_url, path), headers=self.headers
            )
            return response.text
        except requests.exceptions.Timeout:
            print("timeout")
        except requests.exceptions.RequestException as exception:
            print("request exception")
            raise SystemExit(exception) from exception
        return None

    def post(self, path, data=None):
        """Send post request"""
        try:
            response = requests.post(
                "{}{}".format(self.api_url, path), headers=self.headers
            )
            return response.text
        except requests.exceptions.Timeout:
            print("timeout")
        except requests.exceptions.RequestException as exception:
            print("request exception")
            raise SystemExit(exception) from exception
        return None
