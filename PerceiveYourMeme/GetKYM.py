# This file contains of functions
# that are dedicated to get memes, images, news
# from hashes in CONST.py

from typing import Iterable, cast
from urllib.parse import urljoin

import bs4
import urllib3

from .CONST import *
from .MemePage import MemePage
from .NewsPage import NewsPage
from .PhotoPage import PhotoPage


def get_soup(url: str) -> bs4.BeautifulSoup:
    http = urllib3.PoolManager()
    response = http.request("GET", url, headers=HEADERS)
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    return soup


def get_memes(directory: str = "", page_index: int = 1, sort: str = "") -> Iterable[MemePage]:
    # directory : '' or 'popular' or 'submissions'
    # page_index : a positive integer
    # sort : '' or 'views' or 'comments'
    # To return a list of MemePage objects
    url = ""

    if page_index < 1:
        page_index = 1

    if directory == "":
        url = KYM_HASH["memes"] + str(page_index) + MEMES_SORT_HASH[sort]
    else:
        if directory in ["popular", "submissions"]:
            url = MEMES_HASH[directory] + str(page_index) + MEMES_SORT_HASH[sort]
        else:
            url = KYM_HASH["memes"] + str(page_index) + MEMES_SORT_HASH[sort]

    soup = get_soup(url)

    tag_a_list = cast(bs4.Tag, soup.find("table", attrs={"class": "entry_list"})).find_all(
        "a", attrs={"class": "photo"}
    )
    url_list = [urljoin(KYM, tag_a["href"]) for tag_a in tag_a_list]

    return map(MemePage, url_list)


def get_photos(directory: str = "", page_index: int = 1) -> Iterable[PhotoPage]:
    # directory : '' or 'trending' or 'most-commented'
    # page_index : a positive integer
    # To return a list of PhotoPage objects
    url = ""

    if page_index < 1:
        page_index = 1

    if directory == "":
        url = KYM_HASH["photos"] + str(page_index)
    else:
        if directory in ["trending", "most-commented"]:
            url = PHOTOS_HASH[directory] + str(page_index)
        else:
            url = KYM_HASH["photos"] + str(page_index)

    soup = get_soup(url)

    tag_a_list = cast(bs4.Tag, soup.find("div", attrs={"id": "photo_gallery"})).find_all("a", attrs={"class": "photo"})
    url_list = [urljoin(KYM, tag_a["href"]) for tag_a in tag_a_list]

    return map(PhotoPage, url_list)


def get_news(page_index: int = 1) -> Iterable[NewsPage]:
    # page_index : a positive integer
    # To return a list of NewsPage objects
    if page_index < 1:
        page_index = 1

    url = KYM_HASH["news"] + str(page_index)

    soup = get_soup(url)

    url_list = [
        urljoin(KYM, h1.find("a")["href"])
        for h1 in cast(bs4.Tag, soup.find("div", attrs={"id": "maru"})).find_all("div")[1].find_all("h1")
    ]

    return map(NewsPage, url_list)
