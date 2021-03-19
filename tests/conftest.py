"""Test configuration"""

import os

import pytest
from dotenv import load_dotenv

from rival_regions_wrapper import LocalAuthentication, ApiWrapper


load_dotenv()


class MissingAuthenticationError(Exception):
    """Error for missing authentication"""


@pytest.fixture(scope='module')
def vcr(vcr):
    """Set parameters vor VCR"""
    vcr.ignore_localhost = True
    return vcr


@pytest.fixture(scope="module")
def api_wrapper():
    """Set up wrapper before test"""
    username = os.environ.get('USERNAME', None)
    password = os.environ.get('PASSWORD', None)
    login_method = os.environ.get('LOGIN_METHOD', None)
    if None in (username, password, login_method):
        raise MissingAuthenticationError(
            'Load the following variables in your user environment: '
            'username, password, login_method'
        )
    authentication = LocalAuthentication(username, password, login_method)
    return ApiWrapper(authentication)
