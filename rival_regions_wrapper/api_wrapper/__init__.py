"""API wrapper for Rival Regions"""

import os

from dotenv import load_dotenv

from rival_regions_wrapper import RemoteAuthentication, LocalAuthentication


load_dotenv()

USERNAME = os.environ.get('USERNAME', None)
PASSWORD = os.environ.get('PASSWORD', None)
LOGIN_METHOD = os.environ.get('LOGIN_METHOD', None)

API_URL = os.environ.get('API_URL', None)
AUTHORIZATION = os.environ.get('AUTHORIZATION', None)

class MissingEnvironError(Exception):
    """Error for missing environ"""

if None in (USERNAME, PASSWORD, LOGIN_METHOD):
    raise MissingEnvironError(
        'Load the following variables in your user environment: '
        'username, password, login_method'
    )

# api
MIDDLEWARE = RemoteAuthentication(API_URL, AUTHORIZATION)
# MIDDLEWARE = LocalAuthentication(USERNAME,PASSWORD,LOGIN_METHOD)

from .profile import Profile
from .storage import Storage
from .market import Market
from .resource_state import ResourceState
from .perks import Perks
