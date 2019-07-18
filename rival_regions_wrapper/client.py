
"""
Client module
"""

import logging
import re
import time
import requests
from webbot.webbot import Browser
from requests_futures import sessions


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)


class RRClientException(Exception):
    """RR exception"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
    LOGGER.warning('RRClientException')


class Client:
    """class for RR client"""
    resource_id = {
        'oil': 3,
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
        'space stations': 23
    }
    session_id = None
    var_c = None

    def __init__(self, credentials, expires=None, show_window=False):
        self.login_method = credentials['login_method']
        self.username = credentials['username']
        self.password = credentials['password']
        self.expires = expires
        self.show_window = show_window
        LOGGER.info('Init client login_method "%s" username "%s"', self.login_method, self.username)
        if self.login_method in ["g", "google", "v", "vk", "f", "facebook"]:
            self.login()
        else:
            raise RRClientException("Not a valid login method.")

    def login(self):
        """Login user"""
        LOGGER.info('Login in "%s"', self.username)
        login_method = self.login_method
        self.session = requests.Session()
        auth_text = requests.get("http://rivalregions.com").text
        web = Browser(showWindow=self.show_window)

        method_dict = {
            'g': self.login_google,
            'google': self.login_google,
            'v': self.login_vk,
            'vk': self.login_vk,
            'f': self.login_facebook,
            'facebook': self.login_facebook,
        }

        if login_method in method_dict:
            web = method_dict[login_method](web, auth_text)
        else:
            LOGGER.info('Invallid loggin method "%s"', login_method)
        time.sleep(5)

        LOGGER.info('Get cookie')
        sessid = web.get_cookie('PHPSESSID')

        expires = sessid.get('expiry', None)
        sessid.pop('expiry', None)
        sessid.pop('httpOnly', None)
        sessid['expires'] = expires

        web.close_current_tab()
        LOGGER.info('closing login tab')
        self.expires = expires
        self.session_id = sessid
        self.session.cookies.set(**sessid)
        self.set_var_c()

    def login_google(self, web, auth_text):
        """login using Google"""
        LOGGER.info('Login method Google')
        auth_text1 = auth_text.split('\t<a href="')
        auth_text2 = auth_text1[1].split('" class="sa')

        web.go_to(auth_text2[0])
        web.type(self.username, into='Email')
        web.click('Volgende')
        time.sleep(2)
        web.type(self.password, into='Password')
        web.click('Volgende')
        time.sleep(2)

        web.click(css_selector=".sa_sn.float_left.imp.gogo")
        return web

    def login_vk(self, web, auth_text):
        """login using VK"""
        LOGGER.info('Login method VK')
        auth_text1 = auth_text.split("(\'.vkvk\').attr(\'url\', \'")
        auth_text2 = auth_text1[1].split('&response')

        web.go_to(auth_text2[0])
        web.type(self.username, into='email')
        web.type(self.password, xpath="/html/body/div/div/div/div[2]/form/div/div/input[7]")
        web.click('Log in')
        return web

    def login_facebook(self, web, auth_text):
        """login using Facebook"""
        LOGGER.info('Login method Facebook')
        auth_text1 = auth_text.split('">\r\n\t\t\t\t<div class="sa_sn imp float_left" ')
        auth_text2 = auth_text1[0].split('200px;"><a class="sa_link" href="')
        url = auth_text2[1]

        web.go_to(url)
        web.type(self.username, into='Email')
        web.type(self.password, into='Password')
        web.click('Log In')
        time.sleep(5)
        web.click(css_selector='.sa_sn.imp.float_left')
        return web

    def set_var_c(self):
        """Set var_c"""
        LOGGER.info('set the var_c')
        response = self.session.get('http://rivalregions.com/#overview')
        lines = response.text.split("\n")
        for line in lines:
            if re.match("(.*)var c_html(.*)", line):
                self.var_c = line.split("'")[-2]
                return

    def create_article(
            self,
            title,
            article,
            article_lang="en",
            paper_id=0,
            category='0',
            region="4524"
    ):
        """Create new article"""
        response = self.session.get('http://rivalregions.com/#overview')
        response = self.session.post("http://rivalregions.com/news/post", data={
            'c': self.var_c,
            'newspaper': paper_id,
            'category': category,
            'paper': article,
            'title': title,
            'region': region
        })

    def market_info(self, resource, r_id=False):
        """
        Returns a list of data about current resource market state.
        In form price, amount selling, player id, player name string, total offers on market.
        """

        if not r_id:
            res_id = self.resource_id[resource]
        else:
            res_id = resource
        response = self.session.get(f'http://rivalregions.com/storage/market/{res_id}?{self.var_c}')
        return self.parse_market_response(response, res_id)

    def get_all_market_info(self):
        """Request all market info"""
        session = sessions.FuturesSession(session=self.session)
        results = {}
        for type_ in self.resource_id:
            if type_ == 'energy drink':
                continue
            results[type_] = session.get(
                f'http://rivalregions.com/storage/market/{self.resource_id[type_]}?{self.var_c}'
            )
        for res in results:
            result = results[res].result()
            price, selling_amount, player_id, player_name, total_offers = \
                self.parse_market_response(result, self.resource_id[res])
            results[res] = {
                'price': price,
                'amount': selling_amount,
                'player_id': player_id,
                'player_name': player_name,
                'total_offers':total_offers
            }
        return results

    @staticmethod
    def parse_market_response(response, res_id):
        """Parse market response"""
        price = re.search('<input price="(.*)" type', response.text).group(1)
        selling_amount = re.search('<span max="(.*)" url="', response.text).group(1)
        player_id = re.search(
            '<span action="slide/profile/(.*)" class="storage_see pointer dot hov2', response.text
        ).group(1)
        player_name = re.search(
            f'<span action="slide/profile/{player_id}" class="storage_see pointer dot hov2">(.*)</span>',
            response.text
        ).group(1)
        total_offers = re.search(
            f'Best offer out of <span action="storage/listed/{res_id}" class="storage_see pointer hov2"><span class="dot">(.*)</span></span>:',
            response.text
        ).group(1)
        return price, selling_amount, player_id, player_name, total_offers
