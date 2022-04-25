"""Test configuration"""

import os

import pytest
import _pytest.skipping
from dotenv import load_dotenv
from python_anticaptcha import AnticaptchaClient

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
def conference_id():
    """Get conference id from environ variable"""
    value = os.environ.get('CONFERENCE_ID', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: CONFERENCE_ID'
        )
    return value


@pytest.fixture(scope="module")
def message():
    """Get message from environ variable"""
    value = os.environ.get('MESSAGE', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: MESSAGE'
        )
    return value


@pytest.fixture(scope="module")
def conference_title():
    """Get conference title from environ variable"""
    value = os.environ.get('CONFERENCE_TITLE', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: CONFERENCE_TITLE'
        )
    return value


@pytest.fixture(scope="module")
def language_chat():
    """Get language chat from environ varriable"""
    value = os.environ.get('LANGUAGE_CHAT', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: LANGUAGE_CHAT'
        )
    return value


@pytest.fixture(scope="module")
def perk():
    """Get perk from environ varriable"""
    value = os.environ.get('PERK', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: PERK'
        )
    return value


@pytest.fixture(scope="module")
def perk_upgrade_type():
    """Get perk upgrade type from environ varriable"""
    value = os.environ.get('PERK_UPGRADE_TYPE', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: PERK_UPGRADE_TYPE'
        )
    return value


@pytest.fixture(scope="module")
def craft_item():
    """Get craft item from environ varriable"""
    value = os.environ.get('CRAFT_ITEM', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: CRAFT_ITEM'
        )
    return value


@pytest.fixture(scope="module")
def craft_amount():
    """Get craft amount from environ varriable"""
    value = os.environ.get('CRAFT_AMOUNT', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: CRAFT_AMOUNT'
        )
    return value


@pytest.fixture(scope="module")
def profile_id():
    """Get profile id from environ varriable"""
    value = os.environ.get('PROFILE_ID', None)
    if not value:
        raise Exception(
            'Load the following variable in your user environment: PROFILE_ID'
        )
    return value


@pytest.fixture(scope="module")
def middleware():
    """Set up wrapper before test"""
    username = os.environ.get('USERNAME', None)
    password = os.environ.get('PASSWORD', None)
    login_method = os.environ.get('LOGIN_METHOD', None)
    debug = os.environ.get('DEBUG', None)
    captcha_key = os.environ.get('CAPTCHA_KEY', None)
    if None in (username, password, login_method):
        raise MissingAuthenticationError(
            'Load the following variables in your user environment: '
            'USERNAME, PASSWORD, LOGIN_METHOD'
        )
    _middleware = LocalAuthentication(
            False, AnticaptchaClient(captcha_key), debug
        )
    return _middleware.set_credentials(
            username, password, login_method
        )
