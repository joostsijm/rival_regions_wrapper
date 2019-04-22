import asyncio
from webbot.webbot import Browser
import time
import requests
from requests_futures import sessions
import re

class RRBotException(Exception):
    pass


class Client:
    def __init__(self, login_method, username, password, expires=None):
        self.login_method = login_method
        self.username = username
        self.password = password
        self.expires = expires
        self.session_id = None

        if login_method in ["g", "google", "v", "vk", "f", "facebook"]:
            self.login()
        else:
            raise RRBotException("Not a valid login method.")


    def login(self):
        login_method = self.login_method
        self.s = sessions.FuturesSession()
        auth_text = requests.get("http://rivalregions.com").text
        web = Browser(showWindow=False)
        if login_method == ("g" or "google"):
            auth_text1 = auth_text.split('\t<a href="')
            auth_text2 = auth_text1[1].split('" class="sa')

            web.go_to(auth_text2[0])
            web.type(self.username, into='Email')
            web.click('Next')
            time.sleep(5)
            web.type(self.password, into='Password')
            web.click('Next')
            time.sleep(5)

            web.click(css_selector=".sa_sn.float_left.imp.gogo")
            time.sleep(5)
        elif login_method == ("v" or "vk"):
            auth_text1 = auth_text.split("(\'.vkvk\').attr(\'url\', \'")
            auth_text2 = auth_text1[1].split('&response')
            web = Browser(showWindow=False)

            web.go_to(auth_text2[0])
            web.type(self.username, into='email')
            web.type(self.password, xpath="/html/body/div/div/div/div[2]/form/div/div/input[7]")
            web.click('Log in')
            time.sleep(5)

        elif login_method == ("f" or "facebook"):
            auth_text1 = auth_text.split('">\r\n\t\t\t\t<div class="sa_sn imp float_left" ')
            auth_text2 = auth_text1[0].split('200px;"><a class="sa_link" href="')
            url = auth_text2[1]

            web.go_to(url)
            web.type(self.username, into='Email')
            web.type(self.password, into='Password')
            web.click('Log In')
            time.sleep(5)
            web.click(css_selector='.sa_sn.imp.float_left')
            time.sleep(5)

        sessid = web.get_cookie('PHPSESSID')

        expires = sessid.get('expiry', None)
        sessid.pop('expiry', None)
        sessid.pop('httpOnly', None)
        sessid['expires'] = expires

        web.close_current_tab()
        self.expires = expires
        self.session_id = sessid
        self.s.cookies.set(**sessid)
        self.set_c()

    def set_c(self):
        r = self.s.get('http://rivalregions.com/#overview')
        response = r.result()
        lines = response.text.split("\n")
        for line in lines:
            if re.match("(.*)var c_html(.*)", line):
                self.c = line.split("'")[-2]
                return

    async def do_something(self):
        #TODO Get some request done
        pass

