"""
Authentication handler module
"""

import re

import requests
import cfscrape

from rival_regions_wrapper import LOGGER, login_methods
from rival_regions_wrapper.cookie_handler import CookieHandler
from rival_regions_wrapper.browser import Browser
from rival_regions_wrapper.exceptions import InvalidLoginMethodException, \
        SessionExpireException, NoLogginException, NoCookieException


LOGIN_METHOD_DICT = {
    'g': login_methods.login_google,
    'google': login_methods.login_google,
    'v': login_methods.login_vk,
    'vk': login_methods.login_vk,
    'f': login_methods.login_facebook,
    'facebook': login_methods.login_facebook,
}


class AuthenticationHandler:
    """class for RR client"""
    def __init__(self, show_window=False, captcha_client=None):
        LOGGER.info('Initialize, show window: "%s", captcha client: "%s"',
                show_window, bool(captcha_client)
            )
        self.show_window = show_window
        self.captcha_client = captcha_client
        self.login_method = None
        self.username = None
        self.password = None
        self.session = None
        self.var_c = None

    def set_credentials(self, login_method, username, password):
        """Set the credentials"""
        LOGGER.info('"%s": setting credentials, method: "%s"',
                username, login_method
            )
        if login_method not in LOGIN_METHOD_DICT:
            raise InvalidLoginMethodException()
        self.login_method = login_method
        self.username = username
        self.password = password
        self.authenticate()

    def authenticate(self):
        """Login user if needed"""
        LOGGER.info('"%s": start authentication', self.username)
        cookies = CookieHandler.get_cookies(self.username)
        if not cookies:
            LOGGER.info('"%s": No (valid) cookie found, start new login',
                    self.username
                )
            cookies = self.login()
            LOGGER.info('"%s": storing cookie',
                    self.username
                )
            CookieHandler.write_cookies(self.username, cookies)

        self.session = cfscrape.CloudflareScraper()
        for cookie in cookies:
            self.session.cookies.set(**cookie)

        LOGGER.debug('"%s": set the var_c', self.username)
        response = self.session.get('https://rivalregions.com/#overview')
        lines = response.text.split("\n")
        for line in lines:
            if re.match("(.*)var c_html(.*)", line):
                var_c = line.split("'")[-2]
                LOGGER.debug('"%s": got var_c: %s', self.username, var_c)
                self.var_c = line.split("'")[-2]

    def login(self):
        """Login"""
        auth_text = requests.get("https://rivalregions.com").text
        browser = Browser(showWindow=self.show_window)
        browser = LOGIN_METHOD_DICT[self.login_method](
                browser,
                auth_text,
                self.username,
                self.password,
                self.captcha_client
            )

        cookies = []
        for cookie_name in ['PHPSESSID', 'rr_f']:
            browser_cookie = browser.get_cookie(cookie_name)
            if browser_cookie:
                LOGGER.info('"%s": Get "%s" cookie',
                        self.username, cookie_name
                    )
                cookies.append(CookieHandler.create_cookie(
                        cookie_name,
                        browser_cookie.get('expiry', None),
                        browser_cookie.get('value', None)
                    ))
            else:
                raise NoCookieException()

        LOGGER.debug('"%s": closing login tab', self.username)
        browser.close_current_tab()
        return cookies


    def get_browser(self):
        """Get browser"""
        if not self.session:
            raise NoLogginException()

        browser = Browser(showWindow=self.show_window)
        browser.go_to('https://rivalregions.com/')
        for cookie_name, value in \
                self.session.cookies.get_dict().items():
            browser.add_cookie(
                    CookieHandler.create_cookie(cookie_name, None, value)
                )
        return browser
