
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
from webbot.webbot import Browser
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
        LOGGER.warning('why')
        LOGGER.warning('Not logged in')


class NoPHPsessidException(Exception):
    """Raise exception when there is no PHPsessid found"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        LOGGER.warning('No PHPsessid found')


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
            LOGGER.warning('here?')
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
        """Login user if needed"""
        LOGGER.info('"%s": start login, method: "%s"',
                    self.username, self.login_method)
        cookie = self.get_cookie(self.username)
        if cookie is None:
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
                LOGGER.info('Invallid loggin method "%s"', self.login_method)
                sys.exit()

            LOGGER.debug('Get cookie')
            phpsessid = browser.get_cookie('PHPSESSID')
            if phpsessid:
                cookie = self.create_cookie(
                    phpsessid.get('expiry', None),
                    phpsessid.get('value', None)
                )
                self.write_cookie(self.username, cookie)
            else:
                raise NoPHPsessidException()
            LOGGER.debug('closing login tab')
            browser.close_current_tab()

        self.session = cfscrape.CloudflareScraper()
        self.cookie = cookie
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
        LOGGER.info('Login method Google')
        auth_text1 = auth_text.split('\t<a href="')
        auth_text2 = auth_text1[1].split('" class="sa')

        browser.go_to(auth_text2[0])
        LOGGER.info('Typing in username')
        browser.type(self.username, into='Email')
        browser.click('Volgende')
        time.sleep(2)
        LOGGER.info('Typing in password')
        browser.type(self.password, css_selector="input")
        if browser.exists('Sign in'):  # English
            browser.click('Sign in')
        elif browser.exists('Inloggen'):  # Dutch
            browser.click('Inloggen')
        browser.click(css_selector=".sa_sn.float_left.imp.gogo")
        time.sleep(1)
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
    def write_cookie(cls, username, cookie):
        """Write cookie to file"""
        LOGGER.info('Saving cookie for "%s"', username)
        cookies = None
        try:
            with open('{}/cookies.json'.format(DATA_DIR), 'r') as cookies_file:
                cookies = json.load(cookies_file)
        except FileNotFoundError:
            cookies = {}
        cookies[username] = {
            'expires': cookie['expires'],
            'value': cookie['value'],
        }
        with open('{}/cookies.json'.format(DATA_DIR), 'w+') as cookies_file:
            json.dump(cookies, cookies_file)
        LOGGER.info('Saved cookie for "%s"', username)

    @classmethod
    def get_cookie(cls, username):
        """Read cookies for username"""
        LOGGER.info('"%s": Reading cookie', username)
        try:
            with open('{}/cookies.json'.format(DATA_DIR), 'r') as cookies_file:
                cookies = json.load(cookies_file)
                for cookie_username, cookie in cookies.items():
                    if cookie_username == username:
                        LOGGER.info('"%s": Found cookie', username)
                        expires = datetime.fromtimestamp(
                                int(cookie['expires'])
                            )
                        if datetime.now() >= expires:
                            LOGGER.info('"%s": Cookie is expired', username)
                            return None
                        cookie = cls.create_cookie(
                            cookie['expires'],
                            cookie['value'],
                        )
                        return cookie
        except FileNotFoundError:
            pass
        return None

    @classmethod
    def remove_cookie(cls, username):
        """Remove cookie from storage"""
        LOGGER.info('Removing cookie for "%s"', username)
        cookies = None
        try:
            with open('{}/cookies.json'.format(DATA_DIR), 'r') as cookies_file:
                cookies = json.load(cookies_file)
        except FileNotFoundError:
            cookies = {}
        cookies.pop(username, None)
        with open('{}/cookies.json'.format(DATA_DIR), 'w+') as cookies_file:
            json.dump(cookies, cookies_file)
        LOGGER.info('Removed cookie for "%s"', username)

    @staticmethod
    def create_cookie(expires, value):
        """Create cookie"""
        return {
            'domain': 'rivalregions.com',
            'name': 'PHPSESSID',
            'path': '/',
            'secure': False,
            'expires': expires,
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

        LOGGER.debug('"%s" GET: "%s" var_c: %s', self.username, path, add_var_c)
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

        LOGGER.debug('"%s" POST: "%s"', self.username, path)
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
        LOGGER.debug('"%s" CHAT: language %s', self.username, language)
        if self.session:
            response = self.session.get("https://rivalregions.com/#overview")
            if "Session expired, please, reload the page" in response.text:
                raise SessionExpireException()
            browser = Browser(showWindow=self.show_window)
            browser.go_to('https://rivalregions.com/')
            browser.add_cookie(self.get_cookie(self.username))
            browser.go_to(
                    'https://rivalregions.com/#slide/chat/lang_{}'
                    .format(language)
                )
            browser.refresh()
            time.sleep(2)
            browser.type(message, id='message')
            browser.click(id='chat_send')
            LOGGER.info('language %s: finished sending message', language)
            browser.close_current_tab()
        else:
            raise NoLogginException()

    @session_handler
    def send_personal_message(self, user_id, message):
        """send personal message"""
        LOGGER.debug('"%s" PM: user id %s', self.username, user_id)
        if self.session:
            response = self.session.get("https://rivalregions.com/#overview")
            if "Session expired, please, reload the page" in response.text:
                raise SessionExpireException()
            browser = Browser(showWindow=self.show_window)
            browser.go_to('https://rivalregions.com/')
            browser.add_cookie(self.get_cookie(self.username))
            browser.go_to(
                    'https://rivalregions.com/#messages/{}'.format(user_id)
                )
            browser.refresh()
            time.sleep(2)
            browser.type(message, id='message')
            browser.click(id='chat_send')
            LOGGER.info('user %s: finished sending message', user_id)
            browser.close_current_tab()
        else:
            raise NoLogginException()

    @session_handler
    def send_conference_message(self, conference_id, message):
        """send conference message"""
        LOGGER.debug(
                '"%s" CONF: conference id %s',
                self.username, conference_id
            )
        if self.session:
            response = self.session.get("https://rivalregions.com/#overview")
            if "Session expired, please, reload the page" in response.text:
                raise SessionExpireException()
            browser = Browser(showWindow=self.show_window)
            browser.go_to('https://rivalregions.com/')
            browser.add_cookie(self.get_cookie(self.username))
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
                            'conference %s: next message length: %s',
                            conference_id, len(message)
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
        LOGGER.debug(
                '"%s" CONF: conference id %s notification ',
                self.username, conference_id
            )
        data = {
            'sound': 1 if sound else 0,
            'text': message,
            'c': self.var_c
        }

        if self.session:
            LOGGER.info('conference %s: sending notification', conference_id)
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
        return response.text
