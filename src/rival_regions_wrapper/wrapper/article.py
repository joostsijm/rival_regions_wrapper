"""Articl class"""

import unicodedata
import re

from bs4 import BeautifulSoup

from rival_regions_wrapper import util
from rival_regions_wrapper.wrapper.abstract_wrapper import AbstractWrapper


class Article(AbstractWrapper):
    """Wrapper class for article"""

    def info(self, article_id):
        """Get artcile"""
        path = "news/show/{}".format(article_id)
        response = self.middleware.get(path)
        soup = BeautifulSoup(response, "html.parser")

        links = soup.select(".newspaper_links")
        if len(links) >= 3:
            newspaper = links[0]
            author = links[1]
            region = links[2]
        else:
            author = links[0]
            region = links[1]
            newspaper = None

        news_content = soup.select_one(".news_content")

        article_info = {
            "article_id": article_id,
            "article_title": unicodedata.normalize(
                "NFKD", soup.select_one(".title_totr").text
            ),
            "author_name": re.sub(r",\s\skarma.*$", "", author.text),
            "author_id": int(author["action"].replace("slide/profile/", "")),
            "region_name": region.text,
            "region_id": int(region["action"].replace("map/details/", "")),
            "content_text": news_content.get_text(separator="\n", strip=True),
            "content_html": news_content.prettify(),
            "rating": int(soup.select_one("#news_number").text),
            "comments": int(soup.select_one(".news_comments_link").text),
        }

        if newspaper:
            article_info["newspaper_id"] = int(
                newspaper["action"].replace("newspaper/show/", "")
            )
            article_info["newspaper_name"] = newspaper.text
        else:
            article_info["newspaper_id"] = None
            article_info["newspaper_name"] = None

        result = re.search(r".+(\s.+,)", soup.select_one(".tc.small").text)
        try:
            article_info["language"] = re.sub(r"\s|,", "", result[1].strip())
        except IndexError:
            pass

        date_element = soup.select_one(".news_conent_title")
        date_string = date_element.text.replace("✘", "").strip()
        article_info["post_date"] = util.parse_date(date_string)
        return article_info
