import os
from json import dumps
from typing import TypedDict, cast
from urllib.parse import urljoin

import bs4
from urllib3.util import parse_url

from .CONST import DEFAULT_DOWNLOAD_PATH, KYM
from .Request import get


def isValid(url: str) -> bool:
    return "knowyourmeme.com/memes/" in url


MemeInfo = TypedDict(
    "MemeInfo",
    {
        "Title": str,
        "Meme url": str,
        "Header image url": str,
        "Name": str,
        "Unit": str,
        "Status": str,
        "Type": str,
        "Badge": str,
        "Year": list[str],
        "Tags": list[str],
        "Origin": list[str],
        "Region": list[str],
        "Body photos": dict[str, list[str]],
    },
    total=False,
)


class MemePage:
    # An object to store basic information and template of a meme
    def __init__(self, url: str):
        self.url = url
        if isValid(url):
            self.basic_info_dict: MemeInfo = {}
            # Store Meme url
            self.basic_info_dict["Meme url"] = url

            # Name meme
            self.basic_info_dict["Name"] = url.split("/")[-1]

            # Get the html document. This can be slow due to the internet
            response = get(url)
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            try:
                entry_body = cast(bs4.Tag, soup.find("div", attrs={"class": "c", "id": "entry_body"}))
                header = cast(bs4.Tag, soup.find("div", attrs={"id": "maru"})).header
                if header:
                    title = cast(bs4.Tag, header.find("h1"))
                    self.basic_info_dict["Header image url"] = str(header.img["src"]) if header.img else ""

                # Get basic information and entry tags from entry body
                info_dl = cast(bs4.Tag, entry_body.find("dl"))
                keys = [ele.text.strip() for ele in info_dl.find_all(["dt"])]
                values = info_dl.find_all(["dd"])
                basic_info = dict(zip(keys, values))

                tag_dl = cast(bs4.Tag, entry_body.find("dl", attrs={"id": "entry_tags"}))
                entry_tags: list[str] = [ele.text.strip() for ele in tag_dl.find_all("a", attrs={"data-tag": True})]

                def get_text(key: str) -> str:
                    return basic_info[key].text.strip() if key in basic_info else None

                def get_list(key: str):
                    return [ele.text.strip() for ele in basic_info[key].find_all("a")] if key in basic_info else None

                self.basic_info_dict["Title"] = title.text.strip()
                self.basic_info_dict["Status"] = get_text("Status")
                self.basic_info_dict["Type"] = get_list("Type:")
                self.basic_info_dict["Badge"] = get_text("Badges:")
                self.basic_info_dict["Year"] = get_list("Year")
                self.basic_info_dict["Origin"] = get_list("Origin")
                self.basic_info_dict["Region"] = get_list("Region")
                self.basic_info_dict["Tags"] = entry_tags
                # Then store them
                self.basic_info_dict["Unit"] = cast(
                    bs4.Tag, entry_body.find("a", attrs={"class": "entry-category-badge"})
                ).text.strip()

                # Get url of template
                self.org_img_urls = []
                if entry_body.find("center") is not None:
                    imgs = cast(bs4.Tag, entry_body.find("center")).find_all("img")
                    self.org_img_urls = [ele["data-src"] for ele in imgs]

                section = ""
                photos: list[str] = []
                body_photos: dict[str, list[str]] = {}
                for ele in cast(bs4.Tag, entry_body.find("section", attrs={"class": "bodycopy"})).find_all(
                    recursive=False
                ):
                    if ele.name == "h2":
                        if photos:
                            body_photos[section] = photos
                        section = ele.text.strip()
                        photos = []
                    for link in ele.find_all("a"):
                        if link["href"].startswith("/photos/") or "knowyourmeme.com/photos/" in link["href"]:
                            photos.append(urljoin(KYM, link["href"]))
                if photos:
                    body_photos[section] = photos

                self.basic_info_dict["Body photos"] = body_photos
            except Exception as e:
                print(e)
                self.org_img_urls = []

        else:
            print(f"{url} is not a valid meme url")
            self.basic_info_dict = {}
            self.org_img_urls = []

    def pprint(self) -> None:
        print(dumps(self.basic_info_dict, indent=3))

    def save_json(self, custom_path: str = DEFAULT_DOWNLOAD_PATH):
        fname_path = os.path.join(custom_path, self.basic_info_dict["Name"])
        with open(fname_path + ".json", "w", encoding="utf-8") as f:
            f.write(dumps(self.basic_info_dict, indent=2))

    def download_header_image(self, custom_path: str = DEFAULT_DOWNLOAD_PATH) -> bool:
        # Download images
        # then name them corresponding to self.basic_info_dict['Name']
        # Use attributes self.org_img_urls
        url = self.basic_info_dict["Header image url"]
        response = get(url)
        _, ext = os.path.splitext(parse_url(url).path or "")
        ext = ext or "." + response.headers["Content-Type"].split("/")[-1]
        fname_path = os.path.join(custom_path, self.basic_info_dict["Name"])
        with open(fname_path + ext, "wb") as f:
            f.write(response.content)

        return True

    def download_origin_image(self, custom_path: str = DEFAULT_DOWNLOAD_PATH) -> bool:
        # Download images
        # then name them corresponding to self.basic_info_dict['Name']
        # Use attributes self.org_img_urls
        if len(self.org_img_urls) > 0:
            i = 0
            for org_img_url in self.org_img_urls:
                response = get(org_img_url)
                _, ext = os.path.splitext(parse_url(org_img_url).path or "")
                ext = ext or "." + response.headers["Content-Type"].split("/")[-1]
                fname_path = os.path.join(custom_path, self.basic_info_dict["Name"] + " " + str(i))
                with open(fname_path + ext, "wb") as f:
                    f.write(response.content)

                i += 1

            return True

        else:
            print("Org img urls are blank")
            return False
            # If this message shows up,
            # it means that YOU have to add these url manually
            # Use method set_org_img_urls()

    def set_org_img_urls(self, url_list):
        # To change and update
        # attributes self.org_img_urls
        self.org_img_urls = url_list
        self.basic_info_dict["Template urls"] = self.org_img_urls

    def get_org_img_urls(self):
        return self.org_img_urls

    def photos(self, sort: str = "newest", page_index=1) -> list[str]:
        """
        Get photos associated with this meme

        :param sort: 'newest' or 'oldest' or 'comments' or 'favorites' or 'score' or 'low-score' or 'views'
        """

        url = f"{self.url}/photos/sort/{sort}/page/{page_index}"
        response = get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        entries = soup.find("div", attrs={"id": "entries"})
        if entries and entries.find("h3") is not None:
            return []

        photo_gallery = cast(bs4.Tag, soup.find("div", attrs={"id": "photo_gallery"}))
        if not photo_gallery:
            return []

        tag_a_list = photo_gallery.find_all("a", attrs={"class": "photo"})
        url_list = [urljoin(KYM, tag_a["href"]) for tag_a in tag_a_list]
        return url_list


if __name__ == "__main__":
    crying_cat = MemePage("https://knowyourmeme.com/memes/crying-cat")
    crying_cat.pprint()
    # crying_cat.download_origin_image()
