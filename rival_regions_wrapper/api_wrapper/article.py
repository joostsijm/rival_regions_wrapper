"""Articl class"""

import unicodedata
import re

from bs4 import BeautifulSoup

from . import MIDDLEWARE


class Article(object):
    """Wrapper class for profile"""

    @staticmethod
    def info(article_id):
        """Get artcile"""
        path = 'news/show/{}'.format(article_id)
        response = MIDDLEWARE.get(path)
        soup = BeautifulSoup(response, 'html.parser')

        links = soup.select('.newspaper_links')
        newspaper = links[0]
        author = links[1]
        region = links[2]

        news_content = soup.select_one('.news_content')

        article_info = {
            'article_id': article_id,
            'article_title': unicodedata.normalize("NFKD", soup.select_one('.title_totr').text),
            'newspaper_id': int(newspaper['action'].replace('newspaper/show/', '')),
            'newspaper_name': newspaper.text,
            'author_name': re.sub(r',\s\skarma.*$', '', author.text),
            'author_id': int(author['action'].replace('slide/profile/', '')),
            'region_name': region.text,
            'region_id': int(region['action'].replace('map/details/', '')),
            'content_text': news_content.text,
            'content_html': news_content.prettify(),
        }

        result = re.search(r'.+(\s.+,)', soup.select_one('.tc.small').text)
        try:
            article_info['language'] = re.sub(r'\s|,', '', result[1].strip())
        except IndexError:
            pass
        return article_info
