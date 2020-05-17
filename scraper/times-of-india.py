"""
This module scrapes content from Times of India.

It provides:
- get_chronological_headlines(url)

# TODO
- get_trending_headlines(url)
"""

from datetime import datetime
from sys import path
import os
import requests
from bs4 import BeautifulSoup
path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from sources import KNOWN_NEWS_SOURCES
from newscrape_common import ist_to_utc
from datetime import timezone
from dateutil.tz import *


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup.find("div",id="c_articlelist_widgets_1").decompose()

        data = []
        objs = soup.find("div",{"class":"main-content"}).find_all("span", {"class":"w_tle"})

        for obj in objs:
            dt = obj.find_next("span").find("span").get("rodate")
            if dt is not None:
                clean_dt = ist_to_utc(datetime.strptime(dt,"%d %b %Y, %H:%M")).isoformat()

            data.append({
                "link": "https://timesofindia.indiatimes.com"+obj.find("a").get("href"),
                "content": "NA",
                "scraped_at": datetime.now(timezone.utc).astimezone(tz).isoformat(),
                "published_at": clean_dt,
                "title": obj.find("a").get("title")
            })

        return data

def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        x = soup.find("div",{"class":"top-story"})
        y = list(map(
            lambda x: {
                "scraped_at":datetime.utcnow().isoformat(),
                "link":x.get('href')
            },
            filter(
                lambda i : i.get('title') is not None,
                x.find_all('a')
            )
        ))
        # for featured story in left
        x = soup.find("div", id = "featuredstory").find("a")
        y.append(
            {
                "scraped_at":datetime.utcnow().isoformat(),
                "link":x.get('href')
            }
        )
        return y


if __name__ == "__main__":
    import json

    SRC = KNOWN_NEWS_SOURCES["Times of India"]

    print(json.dumps(
        get_chronological_headlines(SRC["pages"].format(2)),
        sort_keys=True,
        indent=4
    ))

    print(json.dumps(
        get_trending_headlines(SRC["home"]),
        sort_keys=True,
        indent=4
    ))
