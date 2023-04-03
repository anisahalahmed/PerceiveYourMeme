import os
from typing import cast

import bs4

from .CONST import DEFAULT_DOWNLOAD_PATH, HEADERS, request


class NewsPage:
    def isValid(self, url: str) -> bool:
        if "/news" in url:
            response = request("GET", url, headers=HEADERS)
            return response.status == 200
        else:
            return False

    # An object to store a news articles
    def __init__(self, url: str) -> None:
        if self.isValid(url):
            self.info_dict = {}
            # Store News url
            self.info_dict["News url"] = url

            # Get the html document. This can be slow due to the internet
            response = request("GET", url, headers=HEADERS)
            soup = bs4.BeautifulSoup(response.data, "html.parser")

            try:
                # Get the super_header information
                super_header = cast(bs4.Tag, soup.find("div", attrs={"id": "super-header"}))
                self.info_dict["Heading"] = super_header.h1.text[1:-1] if super_header.h1 else ""

                t_stmp = cast(bs4.Tag, super_header.find("span", attrs={"class": "header-timestamp"}))
                self.info_dict["Timestamp"] = t_stmp.text[1:-1]

                h_time = cast(bs4.Tag, super_header.find("p", attrs={"class": "header-timestamp"}))
                self.info_dict["Author"] = cast(bs4.Tag, h_time.find("a")).text

                # Get the heading img
                maru = cast(bs4.Tag, soup.find("div", attrs={"id": "maru"}))
                i = cast(bs4.Tag, maru.find("img", attrs={"class": "news-post-header-image"}))
                self.head_img_url = str(i["src"] or i["data-src"])

                # Store url to info_dict
                self.info_dict["Head image url"] = self.head_img_url
            except:
                self.info_dict["Heading"] = ""
                self.info_dict["Timestamp"] = ""
                self.info_dict["Author"] = ""
                self.head_img_url = ""
                self.info_dict["Head image url"] = ""

        else:
            print(f"{url} is not a valid news url")
            self.info_dict = {}
            self.head_img_url = ""

    def pprint(self) -> None:
        # Pretty print of info_dict
        from json import dumps

        print(dumps(self.info_dict, indent=3))

    def download_head_img(self, custom_path: str = DEFAULT_DOWNLOAD_PATH) -> bool:
        # Download photo
        # then name them corresponding to self.info_dict['Head']
        # Use attributes self.head_img_url
        if isinstance(self.head_img_url, str):
            response = request("GET", self.head_img_url, headers=HEADERS)
            if response.status == 200:
                file_type = response.headers["Content-Type"].split("/")[-1]
                fname_path = os.path.join(custom_path, self.info_dict["Heading"])
                with open(fname_path + "." + file_type, "wb") as f:
                    f.write(response.data)

                return True

            else:
                print("Head img url is missing or invalid")
                return False

        else:
            print("Head img url is missing or invalid")
            return False


if __name__ == "__main__":
    random_news = NewsPage(
        "https://news.knowyourmeme.com/news/"
        "mia-khalifa-is-auctioning-iconic-porn-"
        "glasses-to-raise-money-for-beirut"
    )
    random_news.pprint()
    # random_news.download_head_img()
