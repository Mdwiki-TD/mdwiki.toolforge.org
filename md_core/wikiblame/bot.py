"""
python3 pwb.py wikiblame/bot
"""
import requests
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlencode


class WikiBlame:
    """
    A class used to scrape web pages.

    Attributes
    ----------
    base_url : str
        The base URL to scrape.
    params 
        The parameters to add to the base URL.
    content : Optional[str]
        The content of the web page.
    """

    def __init__(self, params):
        self.base_url = "http://wikipedia.ramselehof.de/wikiblame.php"
        self.oldids = []
        self.params = {
            "lang": "",
            "article": "",
            "needle": "",
            "user_lang": "en",
            "project": "wikipedia",
            "tld": "org",
            "skipversions": "0",
            "ignorefirst": "0",
            "limit": "1500",
            "offtag": "22",
            "offmon": "7",
            "offjahr": "2023",
            "searchmethod": "int",
            "order": "desc",
            "force_wikitags": "on",
            "user": ""
        }
        if params is not None:
            self.params.update(params)
        self.content = None

    def fetch_content(self) -> None:
        """Fetch the content of the web page."""
        url = self.base_url + "?" + urlencode(self.params)
        response = requests.get(url)
        self.content = response.text

    def parse_content(self):
        """Parse the content of the web page."""
        if self.content is None:
            print("No content fetched yet. Run fetch_content() first.")
            return None

        soup = BeautifulSoup(self.content, 'html.parser')
        results_div = soup.find("div", {"class": "results"})
        if not results_div:
            print("No results found.")
            return None
        # ---
        results = results_div.find_all("a")
        for x in results:
            href = x.get("href")

            if not href:
                print("No href found.")
                continue
            # match url like https://es.wikipedia.org/w/index.php?title=Letrina_de_hoyo&amp;diff=prev&amp;oldid=87638632
            print(href)
            search = re.search(r"oldid=(\d+)", href)
            if search:
                oldid = search.group(1)
                self.oldids.append(oldid)
        # ---
        return list(set(self.oldids))

    def scrape(self):
        """Scrape the web page with the given parameters."""
        self.fetch_content()
        return self.parse_content()


def get_blame(params):
    scraper = WikiBlame(params)
    return scraper.scrape()


if __name__ == "__main__":
    params = {
        "lang": "es",
        "article": "Letrina de hoyo",
        "needle": "Till2014",
    }
    aa = get_blame(params)
    print(aa)
