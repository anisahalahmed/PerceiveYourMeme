from typing import Iterable, cast
from urllib.parse import urljoin

import bs4

from .CONST import KYM
from .MemePage import MemePage
from .NewsPage import NewsPage
from .PhotoPage import PhotoPage
from .Request import get


def url_maker(context: str, page_index: int, query: str, sort: str):
    return KYM + "/search?context=" + context + "&page=" + str(page_index) + "&q=" + query + "&sort=" + sort


class SearchEntry:
    def __init__(self, query: str, max_pages=1, sort="relevance"):
        self.max_pages = max_pages
        self.query = query
        self.sort = sort

    def search(self) -> list[Iterable[MemePage]]:
        # Scrap this tag <table class="entry_list">
        # To return 2D list of MemePage objects
        # MemePageList[search_page_index][MemePage_index_in_search_page]

        MemePageList: list[Iterable[MemePage]] = []

        for page_index in range(1, self.max_pages + 1):
            url = url_maker("entries", page_index, self.query, self.sort)
            response = get(url)
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            headers3 = cast(bs4.Tag, soup.find("div", attrs={"id": "entries"})).find("h3")
            if headers3 is not None:
                break

            entry_list = cast(bs4.Tag, soup.find("table", attrs={"class": "entry_list"}))
            tag_a_list = entry_list.find_all("a", attrs={"class": "photo"})
            url_list = [urljoin(KYM, tag_a["href"]) for tag_a in tag_a_list]
            MemePageList.append(map(MemePage, url_list))

        return MemePageList


class SearchImage:
    def __init__(self, query: str, max_pages=1, sort="relevance"):
        self.max_pages = max_pages
        self.query = query
        self.sort = sort

    def search(self) -> list[Iterable[PhotoPage]]:
        # Scrap this tag <div id="photo_gallery">
        # To return 2D list of PhotoPage objects
        # PhotoPageList[search_page_index][PhotoPage_index_in_search_page]

        # If use this to get multiple images,
        # name of PhotoPage onject will be blank

        PhotoPageList: list[Iterable[PhotoPage]] = []

        for page_index in range(1, self.max_pages + 1):
            url = url_maker("images", page_index, self.query, self.sort)
            response = get(url)
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            entries = cast(bs4.Tag, soup.find("div", attrs={"id": "entries"}))
            if entries.find("h3") is not None:
                break

            photo_gallery = cast(bs4.Tag, soup.find("div", attrs={"id": "photo_gallery"}))
            tag_a_list = photo_gallery.find_all("a", attrs={"class": "photo"})
            url_list = [urljoin(KYM, tag_a["href"]) for tag_a in tag_a_list]
            PhotoPageList.append(map(PhotoPage, url_list))

        return PhotoPageList


class SearchNews:
    def __init__(self, query: str, max_pages=1, sort="relevance"):
        self.max_pages = max_pages
        self.query = query
        self.sort = sort

    def search(self) -> list[Iterable[NewsPage]]:
        # Srap this tag # <div id="news-posts">
        # To return 2D list of NewsPages objects
        # NewsPageList[search_page_index][NewsPage_index_in_search_page]

        NewsPageList: list[Iterable[NewsPage]] = []

        for page_index in range(1, self.max_pages + 1):
            url = url_maker("news", page_index, self.query, self.sort)
            response = get(url)
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            headers3 = cast(bs4.Tag, soup.find("div", attrs={"id": "entries"})).h3
            if headers3 is not None:
                break

            entries = cast(bs4.Tag, soup.find("div", attrs={"id": "entries"}))
            headers1 = entries.find_all("div")[1].find_all("h1")
            url_list = [urljoin(KYM, h1.find("a")["href"]) for h1 in headers1]
            NewsPageList.append(map(NewsPage, url_list))

        return NewsPageList


class SearchEngine:
    # A class to search for MemePage, PhotoPage, VideoPage
    def __init__(self, query: str, context="entries", max_pages=1, sort="relevance"):
        # context : 'entries' or 'images' or 'news'
        # max_pages : a positive number
        # query : a string, for example 'Elon Musk'
        # sort : 'relevance' or 'views' or 'newest' or 'oldest'

        if max_pages < 1:
            self.max_pages = 1
        else:
            self.max_pages = max_pages

        if context not in ["entries", "images", "news"]:
            self.context = "entries"
        else:
            self.context = context

        if sort not in ["relevance", "views", "newest", "oldest"]:
            self.sort = "relevance"
        else:
            self.sort = sort

        if isinstance(query, str) and query != "":
            # Format query to have the valid format
            self.query = query.replace(" ", "+", -1)
        else:
            print("Query is not a string")
            self.query = ""

    def build(self):
        # Build object SearchEntry, SearchImage, SearchNews
        if self.query == "":
            print("No object is build")
            return None
        else:
            if self.context == "entries":
                return SearchEntry(query=self.query, max_pages=self.max_pages, sort=self.sort)

            if self.context == "images":
                return SearchImage(query=self.query, max_pages=self.max_pages, sort=self.sort)

            if self.context == "news":
                return SearchNews(query=self.query, max_pages=self.max_pages, sort=self.sort)
