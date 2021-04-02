"""middleware class"""

from abc import ABC, abstractmethod

import requests

from rival_regions_wrapper import AuthenticationHandler


class MiddlewareBase(ABC):
    """Middleware abstract base class"""

    @abstractmethod
    def get(self, path, add_c_var=False):
        """Send get request"""

    @abstractmethod
    def post(self, path, data=None):
        """Send post request"""

    @abstractmethod
    def send_conference_message(self, conference_id, message):
        """Send conference message"""

    @abstractmethod
    def send_conference_notification(self, conference_id, message, sound):
        """Send conference notification"""

class LocalAuthentication(MiddlewareBase):
    """Local authentication"""

    def __init__(self, username, password, login_method, show_window=False):
        self.client = AuthenticationHandler(show_window)
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

    def send_conference_message(self, conference_id, message):
        """Send conference message"""
        return self.client.send_conference_message(conference_id, message)

    def send_conference_notification(self, conference_id, message, sound):
        """Send conference notification"""
        return self.client.send_conference_notification(conference_id, message, sound)

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
            raise SystemExit(exception) from exception
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
            raise SystemExit(exception) from exception
        return None
