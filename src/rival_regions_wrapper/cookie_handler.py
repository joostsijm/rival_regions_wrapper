"""
Store and retrieve cookies
"""

from datetime import datetime
import json

from rival_regions_wrapper import LOGGER, DATA_DIR


class CookieHandler:
    """Cookie handler class"""

    @classmethod
    def write_cookies(cls, username, passed_cookies):
        """Write cookie to file"""
        LOGGER.info('"%s": Saving cookie', username)
        cookies = None
        try:
            with open(
                "{}/cookies.json".format(DATA_DIR), "r"
            ) as cookies_file:
                cookies = json.load(cookies_file)
            if not cookies:
                raise FileNotFoundError
        except FileNotFoundError:
            cookies = {username: {}}
        if username not in cookies:
            cookies[username] = {}
        for cookie in passed_cookies:
            cookies[username][cookie["name"]] = {
                "expiry": cookie["expires"],
                "value": cookie["value"],
            }

        with open("{}/cookies.json".format(DATA_DIR), "w+") as cookies_file:
            json.dump(cookies, cookies_file)
        LOGGER.info('"%s": Saved cookie', username)

    @classmethod
    def get_cookies(cls, username):
        """Read cookies for username"""
        LOGGER.info('"%s": Searching for cookie', username)
        cookies = []
        try:
            with open(
                "{}/cookies.json".format(DATA_DIR), "r"
            ) as cookies_file:
                cookies_data = json.load(cookies_file)
                for cookie_username, user_cookies in cookies_data.items():
                    if cookie_username == username:
                        LOGGER.info('"%s": Found cookie', username)
                        for cookie_name, cookie in user_cookies.items():
                            expires = datetime.fromtimestamp(
                                int(cookie["expiry"])
                            )
                            if datetime.now() >= expires:
                                LOGGER.info(
                                    '"%s": Cookie is expired', username
                                )
                                return cookies
                            cookies.append(
                                cls.create_cookie(
                                    cookie_name,
                                    cookie["expiry"],
                                    cookie["value"],
                                )
                            )
                        return cookies
        except FileNotFoundError:
            pass
        return cookies

    @classmethod
    def remove_cookie(cls, username):
        """Remove cookie from storage"""
        LOGGER.info('"%s": Removing cookie', username)
        cookies = None
        try:
            with open(
                "{}/cookies.json".format(DATA_DIR), "r"
            ) as cookies_file:
                cookies = json.load(cookies_file)
        except FileNotFoundError:
            cookies = {}
        cookies.pop(username, None)
        with open("{}/cookies.json".format(DATA_DIR), "w+") as cookies_file:
            json.dump(cookies, cookies_file)
        LOGGER.info('"%s": Removed cookie', username)

    @staticmethod
    def create_cookie(name, expiry, value):
        """Create cookie"""
        return {
            "domain": "rivalregions.com",
            "name": name,
            "path": "/",
            "secure": False,
            "expires": expiry,
            "value": value,
        }
