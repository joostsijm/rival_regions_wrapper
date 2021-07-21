"""
Exceptions used in Rival Regions Wrapper
"""

from rival_regions_wrapper import LOGGER


class InvalidLoginMethodException(Exception):
    """Raise exception when login method is invalid"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning("Login method invalid")


class RRClientException(Exception):
    """RR exception"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning("RRClientException")


class SessionExpireException(Exception):
    """Raise when session has expired"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning("Session has expired")


class NoLogginException(Exception):
    """Raise exception when client isn't logged in"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning("Not logged in")


class NoCookieException(Exception):
    """Raise exception when there is no cookie found"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning("No cookie found")


class NoCaptchaClientException(Exception):
    """Raise exception when captcha client is missing"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning("No Captcha client given")


class LoginException(Exception):
    """Raise exception when there is an error during login"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning("Error during login")
