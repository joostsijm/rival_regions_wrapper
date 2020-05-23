"""middleware class"""

from abc import ABC, abstractmethod

import requests

from .authentication_handler import AuthenticationHandler


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
        self.client = AuthenticationHandler()
        self.client.set_credentials({
            'username': username,
            'password': password,
            'login_method': login_method
        })
        super().__init__()

    def get(self, path, add_c_var=False):
        """Send get requests"""
        return self.client.get(path)

    def post(self, path, data=None):
        """Send post request"""
        return self.client.post(path, data=data)


class RemoteAuthentication(MiddlewareBase):
    """Remote authentication"""

    def __init__(self, api_url, authentication_key):
        self.api_url = api_url
        self.headers = {
            'Authorization': authentication_key
        }
        super().__init__()

    def get(self, path, add_c_var=False):
        """Send get requests"""
        try:
            response = requests.get(
                '{}{}'.format(self.api_url, path), headers=self.headers
            )
            return response.text
        except requests.exceptions.Timeout:
            print('timeout')
        except requests.exceptions.RequestException as exception:
            print('request exception')
            raise SystemExit(exception)
        return None

    def post(self, path, data=None):
        """Send post request"""
        try:
            response = requests.post(
                '{}{}'.format(self.api_url, path), headers=self.headers
            )
            return response.text
        except requests.exceptions.Timeout:
            print('timeout')
        except requests.exceptions.RequestException as exception:
            print('request exception')
            raise SystemExit(exception)
        return None
