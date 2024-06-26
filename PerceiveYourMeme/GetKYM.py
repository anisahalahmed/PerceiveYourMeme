# This file contains of functions
# that are dedicated to get memes, images, news
# from hashes in CONST.py

from typing import cast
from urllib.parse import urljoin

import bs4

from .CONST import KYM, KYM_HASH, PHOTOS_HASH
from .Request import get


def get_soup(url: str) -> bs4.BeautifulSoup:
    response = get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return soup


def get_memes(category: str = "", directory: str = "confirmed", page_index: int = 1, sort: str = "newest") -> list[str]:
    """
    Returns a list of MemePage objects

    :param directory: 'confirmed' or 'popular' or 'submissions'
    :param page_index: a positive integer
    :param sort: 'newest' or 'oldest' or 'views' or 'comments' or 'chronological' or 'reverse-chronological' or 'images' or 'videos'
    """
    url = ""

    if page_index < 1:
        page_index = 1

    url = (
        KYM_HASH["category"] + category + "/page/" + str(page_index) + "?status=" + directory + "&sort=" + sort
        if category
        else KYM_HASH["memes"] + directory + "/page/" + str(page_index) + "?sort=" + sort
    )

    soup = get_soup(url)

    tag_a_list = cast(bs4.Tag, soup.find("table", attrs={"class": "entry_list"})).find_all(
        "a", attrs={"class": "photo"}
    )
    url_list = [urljoin(KYM, tag_a["href"]) for tag_a in tag_a_list]

    return url_list


def get_photos(directory: str = "", page_index: int = 1) -> list[str]:
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

    return url_list


def get_news(page_index: int = 1) -> list[str]:
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

    return url_list
