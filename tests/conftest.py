"""Test configuration"""

import os

import pytest
import _pytest.skipping
from dotenv import load_dotenv

from rival_regions_wrapper.middleware import LocalAuthentication


load_dotenv()


class MissingAuthenticationError(Exception):
    """Error for missing authentication"""


def pytest_addoption(parser):
    """Add option to parser to prevent skips"""
    parser.addoption(
        "--no-skips",
        action="store_true",
        default=False, help="disable skip marks")


@pytest.hookimpl(tryfirst=True)
def pytest_cmdline_preparse(config, args):
    """Add check for skips"""
    if "--no-skips" not in args:
        return

    def no_skip(*args, **kwargs):
        return

    _pytest.skipping.skip = no_skip


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
    return LocalAuthentication(username, password, login_method)
