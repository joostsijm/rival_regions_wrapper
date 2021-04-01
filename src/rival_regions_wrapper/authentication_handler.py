
"""
Client module
"""

import sys
import logging
import re
import time
from datetime import datetime
import json
import pathlib2

import requests
import cfscrape
from .browser import StealthBrowser as Browser
from appdirs import user_data_dir


DATA_DIR = user_data_dir('rival_regions_wrapper', 'bergc')
pathlib2.Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# get logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# create file handler
FILE_HANDLER = logging.FileHandler('{}/output.log'.format(DATA_DIR))
FILE_HANDLER.setLevel(logging.DEBUG)

# create console handler
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)

# create formatter and add it to the handlers
STREAM_FORMATTER = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
STREAM_HANDLER.setFormatter(STREAM_FORMATTER)
FILE_FORMATTER = logging \
        .Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FILE_HANDLER.setFormatter(FILE_FORMATTER)

# add the handlers to logger
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)


class RRClientException(Exception):
    """RR exception"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning('RRClientException')


class SessionExpireException(Exception):
    """Raise when session has expired"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning('Session has expired')


class NoLogginException(Exception):
    """Raise exception when client isn't logged in"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning('Not logged in')


class NoCookieException(Exception):
    """Raise exception when there is no cookie found"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning('No cookie found')


def session_handler(func):
    """Handle expired sessions"""
    def wrapper(*args, **kwargs):
        instance = args[0]
        return try_run(instance, func, *args, **kwargs)

    def try_run(instance, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (SessionExpireException, ConnectionError, ConnectionResetError):
            instance.remove_cookie(instance.username)
            instance.login()
            return try_run(instance, func, *args, **kwargs)
        except NoLogginException:
            instance.login()
            return try_run(instance, func, *args, **kwargs)

    return wrapper


class AuthenticationHandler:
    """class for RR client"""
    cookie = None
    var_c = None
    login_method = None
    username = None
    password = None
    session = None

    def __init__(self, show_window=False):
        self.show_window = show_window
        self.LOGGER = LOGGER
        LOGGER.info('Initialize authentication handler, show window: "%s"',
                    self.show_window)

    def set_credentials(self, credentials):
        """Set the credentials"""
        LOGGER.info('"%s": setting credentials', credentials['username'])
        self.login_method = credentials['login_method']
        self.username = credentials['username']
        self.password = credentials['password']
        self.login()

    def login(self):
        self.remove_cookie(self.username)
        """Login user if needed"""
        LOGGER.info('"%s": start login, method: "%s"',
                    self.username, self.login_method)
        cookies = self.get_cookies(self.username)
        if not cookies:
            LOGGER.info('"%s": no cookie, new login, method "%s"',
                        self.username, self.login_method)
            if self.login_method not in [
                        "g", "google", "v", "vk", "f", "facebook"
                    ]:
                raise RRClientException("Not a valid login method.")

            auth_text = requests.get("https://rivalregions.com").text
            browser = Browser(showWindow=self.show_window)

            method_dict = {
                'g': self.login_google,
                'google': self.login_google,
                'v': self.login_vk,
                'vk': self.login_vk,
                'f': self.login_facebook,
                'facebook': self.login_facebook,
            }

            if self.login_method in method_dict:
                browser = method_dict[self.login_method](browser, auth_text)
            else:
                LOGGER.info(
                        '"%s": Invalid login method "%s"',
                        self.username, self.login_method
                    )
                sys.exit()

            LOGGER.info('"%s": Get PHPSESSID', self.username)
            browser_cookie = browser.get_cookie('PHPSESSID')
            if browser_cookie:
                expiry = browser_cookie.get('expiry', None)
                value = browser_cookie.get('value', None)
                LOGGER.info('"{}": "value": {}, "expiry": {}'.format(
                        self.username, value, expiry
                    ))
                cookie = self.create_cookie(
                        'PHPSESSID',
                        expiry,
                        value
                    )
                cookies.append(cookie)
            else:
                raise NoCookieException()

            # TODO: what's up with 'rival/googles'

            cookie_names = ['rr_f']
            for cookie_name in cookie_names:
                browser_cookie = browser.get_cookie(cookie_name)
                if browser_cookie:
                    LOGGER.info('"{}": Get {}'.format(
                        self.username, cookie_name
                    ))
                    expiry = browser_cookie.get('expiry', None)
                    value = browser_cookie.get('value', None)
                    cookies.append(
                        self.create_cookie(
                            cookie_name,
                            expiry,
                            value
                        )
                    )
                    LOGGER.info('"{}": "value": {}, "expiry": {}'.format(
                            self.username, value, expiry
                        ))
                else:
                    raise NoCookieException()

            self.write_cookies(self.username, cookies)
            LOGGER.debug('"%s": closing login tab', self.username)
            browser.close_current_tab()
        else:
            LOGGER.info('Cookies found')

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

    # This is working
    def login_google(self, browser, auth_text):
        """login using Google"""
        LOGGER.info('"%s": Login method Google', self.username)
        auth_text1 = auth_text.split('\t<a href="')
        auth_text2 = auth_text1[1].split('" class="sa')
        time.sleep(1)
        browser.go_to(auth_text2[0])

        LOGGER.info('"%s": Typing in username', self.username)
        browser.type(self.username, into='Email')

        LOGGER.info('"%s": pressing next button', self.username)
        browser.click(css_selector="#next")
        time.sleep(2)

        LOGGER.info('"%s": Typing in password', self.username)
        browser.type(self.password, css_selector="input")

        LOGGER.info('"%s": pressing sign in button', self.username)
        browser.click(css_selector="#submit")
        time.sleep(3)

        # Some why it wont click and login immediately. This seems to work
        time.sleep(1)
        browser.go_to(auth_text2[0])
        time.sleep(1)
        browser.go_to(auth_text2[0])
        time.sleep(1)
        browser.click(css_selector="#sa_add2 > div:nth-child(4) > a.sa_link.gogo > div")
        time.sleep(3)
        return browser

    # IDK if this is working
    def login_vk(self, browser, auth_text):
        """login using VK"""
        LOGGER.info('Login method VK')
        auth_text1 = auth_text.split("(\'.vkvk\').attr(\'url\', \'")
        auth_text2 = auth_text1[1].split('&response')

        browser.go_to(auth_text2[0])
        browser.type(self.username, into='email')
        browser.type(
                self.password,
                xpath="/html/body/div/div/div/div[2]/form/div/div/input[7]"
        )
        browser.click('Log in')
        return browser

    # IDK if this is working
    def login_facebook(self, browser, auth_text):
        """login using Facebook"""
        LOGGER.info('Login method Facebook')
        auth_text1 = \
            auth_text.split('">\r\n\t\t\t\t<div class="sa_sn imp float_left" ')
        auth_text2 = auth_text1[0].split('200px;"><a class="sa_link" href="')
        url = auth_text2[1]

        browser.go_to(url)
        browser.type(self.username, into='Email')
        browser.type(self.password, into='Password')
        browser.click('Log In')
        time.sleep(5)
        browser.click(css_selector='.sa_sn.imp.float_left')
        return browser

    @classmethod
    def write_cookies(cls, username, passed_cookies):
        """Write cookie to file"""
        LOGGER.info('"%s": Saving cookie', username)
        cookies = None
        try:
            with open('{}/cookies.json'.format(DATA_DIR), 'r') as cookies_file:
                cookies = json.load(cookies_file)
            if not cookies:
                raise FileNotFoundError # raise error as if file hadn't been found
        except FileNotFoundError:
            cookies = {username : {}}
        if username not in cookies:
            cookies[username] = {}
        for cookie in passed_cookies:
            cookies[username][cookie['name']] = {
                'expiry': cookie['expires'],
                'value': cookie['value'],
            }

        with open('{}/cookies.json'.format(DATA_DIR), 'w+') as cookies_file:
            json.dump(cookies, cookies_file)
        LOGGER.info('"%s": Saved cookie for', username)

    @classmethod
    def get_cookies(cls, username):
        """Read cookies for username"""
        LOGGER.info('"%s": Reading cookie', username)
        cookies = []
        try:
            with open('{}/cookies.json'.format(DATA_DIR), 'r') as cookies_file:
                cookies_data = json.load(cookies_file)
                for cookie_username, user_cookies in cookies_data.items():
                    if cookie_username == username:
                        LOGGER.info('"%s": Found cookies', username)
                        for cookie_name, cookie in user_cookies.items():
                            expires = datetime.fromtimestamp(
                                    int(cookie['expiry'])
                                )
                            if datetime.now() >= expires:
                                LOGGER.info('"%s": Cookie is expired', username)
                                return None
                            cookies.append(cls.create_cookie(
                                cookie_name,
                                cookie['expiry'],
                                cookie['value'],
                            ))
                        return cookies
        except FileNotFoundError:
            pass
        return cookies

    @classmethod
    def remove_cookie(cls, username):
        """Remove cookie from storage"""
        LOGGER.info('"%s": Removing cookie for', username)
        cookies = None
        try:
            with open('{}/cookies.json'.format(DATA_DIR), 'r') as cookies_file:
                cookies = json.load(cookies_file)
        except FileNotFoundError:
            cookies = {}
        cookies.pop(username, None)
        with open('{}/cookies.json'.format(DATA_DIR), 'w+') as cookies_file:
            json.dump(cookies, cookies_file)
        LOGGER.info('"%s": Removed cookie', username)

    @staticmethod
    def create_cookie(name, expiry, value):
        """Create cookie"""
        return {
            'domain': 'rivalregions.com',
            'name': name,
            'path': '/',
            'secure': False,
            'expires': expiry,
            'value': value,
        }

    @session_handler
    def get(self, path, add_var_c=False):
        """Send get request to Rival Regions"""
        if path[0] == '/':
            path = path[1:]

        params = {}
        if add_var_c:
            params['c'] = self.var_c

        LOGGER.info(
                '"%s" GET: "%s" var_c: %s', self.username, path, add_var_c
            )
        if self.session:
            response = self.session.get(
                url='https://rivalregions.com/{}'.format(path),
                params=params
            )
            if "Session expired, please, reload the page" \
                    in response.text or \
                    'window.location="https://rivalregions.com";' \
                    in response.text:
                raise SessionExpireException()
        else:
            raise NoLogginException()
        return response.text

    @session_handler
    def post(self, path, data=None):
        """Send post request to Rival Regions"""
        if path[0] == '/':
            path = path[1:]
        if not data:
            data = {}
        data['c'] = self.var_c

        LOGGER.info('"%s" POST: "%s"', self.username, path)
        if self.session:
            response = self.session.post(
                "https://rivalregions.com/{}".format(path),
                data=data
            )
            if "Session expired, please, reload the page" \
                    in response.text or \
                    'window.location="https://rivalregions.com";' \
                    in response.text:
                raise SessionExpireException()
        else:
            raise NoLogginException()
        return response.text

    @session_handler
    def send_chat(self, language, message):
        """send chat message"""
        LOGGER.info('"%s" CHAT: language %s', self.username, language)
        if self.session:
            response = self.session.get("https://rivalregions.com/#overview")
            if "Session expired, please, reload the page" in response.text:
                raise SessionExpireException()
            browser = Browser(showWindow=self.show_window)
            browser.go_to('https://rivalregions.com/')
            for cookie in self.get_cookies(self.username):
                browser.add_cookie(cookie)
            browser.go_to(
                    'https://rivalregions.com/#slide/chat/lang_{}'
                    .format(language)
                )
            browser.refresh()
            time.sleep(2)
            browser.type(message, id='message')
            browser.click(id='chat_send')
            LOGGER.info(
                '"%s" CHAT: language %s, finished sending message',
                self.username, language
            )
            browser.close_current_tab()
        else:
            raise NoLogginException()

    @session_handler
    def send_personal_message(self, user_id, message):
        """send personal message"""
        LOGGER.info('"%s" PM: user id %s', self.username, user_id)
        if self.session:
            response = self.session.get("https://rivalregions.com/#overview")
            if "Session expired, please, reload the page" in response.text:
                raise SessionExpireException()
            browser = Browser(showWindow=self.show_window)
            browser.go_to('https://rivalregions.com/')
            for cookie in self.get_cookies(self.username):
                browser.add_cookie(cookie)
            browser.go_to(
                    'https://rivalregions.com/#messages/{}'.format(user_id)
                )
            browser.refresh()
            time.sleep(2)
            browser.type(message, id='message')
            browser.click(id='chat_send')
            LOGGER.info(
                    '"%s" PM: user id %s, finished sending message',
                    self.username, user_id)
            browser.close_current_tab()
        else:
            raise NoLogginException()

    @session_handler
    def send_conference_message(self, conference_id, message):
        """send conference message"""
        LOGGER.info(
                '"%s" CONF: id %s',
                self.username, conference_id
            )
        if self.session:
            response = self.session.get("https://rivalregions.com/#overview")
            if "Session expired, please, reload the page" in response.text:
                raise SessionExpireException()
            browser = Browser(showWindow=self.show_window)
            browser.go_to('https://rivalregions.com/')
            for cookie in self.get_cookies(self.username):
                browser.add_cookie(cookie)
            browser.go_to(
                    'https://rivalregions.com/#slide/conference/{}'
                    .format(conference_id)
                )
            browser.refresh()
            time.sleep(2)

            character_count = 0
            tmp_messages = []
            for sentence in message.split('\n'):
                sentence_character_count = 0
                tmp_sentence = []
                for word in sentence.split(' '):
                    sentence_character_count += len(word) + 1
                    if sentence_character_count >= 899:
                        message = '{}\n{}'.format('\n'.join(
                                tmp_messages),
                                ' '.join(tmp_sentence)
                            )
                        LOGGER.info(
                                '"%s" CONF: id %s, next message length: %s',
                                self.username, conference_id, len(message)
                            )
                        browser.type(message, id='message')
                        browser.click(id='chat_send')
                        sentence_character_count = 0
                        tmp_sentence = []
                        character_count = 0
                        tmp_messages = []
                    tmp_sentence.append(word)

                sentence = ' '.join(tmp_sentence)
                character_count += len(sentence) + 1
                if character_count >= 900:
                    message = '\n'.join(tmp_messages)
                    LOGGER.info(
                        'conference %s: next message length: %s',
                        conference_id, len(message)
                    )
                    browser.type(message, id='message')
                    browser.click(id='chat_send')
                    character_count = 0
                    tmp_messages = []
                tmp_messages.append(sentence)

            if tmp_messages:
                message = '\n'.join(tmp_messages)
                LOGGER.info(
                        'conference %s: next message length: %s',
                        conference_id, len(message)
                    )
                browser.type(message, id='message')
                browser.click(id='chat_send')

            LOGGER.info(
                    'conference %s: finished sending message',
                    conference_id
                )
            browser.close_current_tab()
        else:
            raise NoLogginException()

    @session_handler
    def send_conference_notification(self, conference_id, message, sound):
        """send conference notification"""
        LOGGER.info(
                '"%s" CONF: id %s notification ',
                self.username, conference_id
            )
        data = {
            'sound': 1 if sound else 0,
            'text': message,
            'c': self.var_c
        }

        if self.session:
            response = self.session.post(
                "https://rivalregions.com/rival/konffcm/{}/".format(
                    conference_id
                ),
                data=data
            )
            if "Session expired, please, reload the page" \
                    in response.text or \
                    'window.location="https://rivalregions.com";' \
                    in response.text:
                raise SessionExpireException()
        else:
            raise NoLogginException()
        LOGGER.info(
                '"%s" CONF: id %s send notification ',
                self.username, conference_id
            )
        return response.text
