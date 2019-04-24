import asyncio
from webbot.webbot import Browser
import time
from lxml import html
from lxml import etree
import requests
from requests_futures import sessions
import re

class RRBotException(Exception):
    pass


class Client:
    def __init__(self, login_method, username, password, expires=None, show_window=False):
        self.login_method = login_method
        self.username = username
        self.password = password
        self.expires = expires
        self.resource_id = {'oil': 3,
                            'ore': 4,
                            'uranium': 11,
                            'diamond': 15,
                            'liquid oxygen': 21,
                            'helium-3': 24,
                            'antirad': 13,
                            'energy drink': 17,
                            'spacerockets': 20,
                            'tanks': 2,
                            'aircrafts': 1,
                            'missiles': 14,
                            'bombers': 16,
                            'battleships': 18,
                            'moon tanks': 22,
                            'space stations': 23}
        self.session_id = None
        self.c = None
        self.show_window = show_window

        if login_method in ["g", "google", "v", "vk", "f", "facebook"]:
            self.login()
        else:
            raise RRBotException("Not a valid login method.")

    def login(self):
        login_method = self.login_method
        self.s = requests.Session()
        auth_text = requests.get("http://rivalregions.com").text
        web = Browser(showWindow=self.show_window)
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
        lines = r.text.split("\n")
        for line in lines:
            if re.match("(.*)var c_html(.*)", line):
                self.c = line.split("'")[-2]
                return

    def create_article(self, title, article, article_lang="en", paper_id=0, category='0', region="4524"):
        r = self.s.get('http://rivalregions.com/#overview')
        r = self.s.post("http://rivalregions.com/news/post", data={"c":self.c,
                                                                   'newspaper': paper_id,
                                                                   'category': category,
                                                                   'paper': article,
                                                                   'title': title,
                                                                   'region': region})

    def market_info(self, resource, r_id=False):
        """
        Returns a list of data about current resource market state.
        In form price, amount selling, player id, player name string, total offers on market.
        """

        if not r_id:
            res_id = self.resource_id[resource]
        else:
            res_id = resource
        r = self.s.get(f'http://rivalregions.com/storage/market/{res_id}?{self.c}')
        return self.parse_market_response(r, res_id)

    def get_all_market_info(self):
        session = sessions.FuturesSession(session=self.s)
        results = {}
        for type_ in self.resource_id:
            if type_ == 'energy drink':
                continue
            results[type_] = session.get(f'http://rivalregions.com/storage/market/{self.resource_id[type_]}?{self.c}')
        for res in results:
            r = results[res].result()
            price, selling_amount, player_id, player_name, total_offers = self.parse_market_response(r, self.resource_id[res])
            results[res] = {'price': price,
                            'amount': selling_amount,
                            'player_id': player_id,
                            'player_name': player_name,
                            'total_offers':total_offers}
        return results

    @staticmethod
    def parse_market_response(r, res_id):
        price = re.search('<input price="(.*)" type', r.text).group(1)
        selling_amount = re.search('<span max="(.*)" url="', r.text).group(1)
        player_id = re.search('<span action="slide/profile/(.*)" class="storage_see pointer dot hov2', r.text).group(1)
        player_name = re.search(f'<span action="slide/profile/{player_id}" class="storage_see pointer dot hov2">(.*)</span>', r.text).group(1)
        total_offers = re.search(f'Best offer out of <span action="storage/listed/{res_id}" class="storage_see pointer hov2"><span class="dot">(.*)</span></span>:', r.text).group(1)
        return price, selling_amount, player_id, player_name, total_offers


