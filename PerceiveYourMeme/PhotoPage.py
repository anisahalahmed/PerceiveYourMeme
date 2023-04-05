import os
from json import dumps
from typing import TypedDict, cast
from urllib.parse import urljoin
from urllib3.util import parse_url

import bs4
from dateutil.parser import parse

from .CONST import DEFAULT_DOWNLOAD_PATH, KYM
from .Request import get


def isValid(url):
    # type: (str) -> bool
    """Checks if given url is a valid know your meme photo url"""
    return "knowyourmeme.com/photos/" in url


PhotoInfo = TypedDict(
    "PhotoInfo",
    {
        "Id": str,
        "Name": str,
        "Title": str,
        "Meme": str,
        "Meme url": str,
        "Uploaded": int,
        "Tags": list[str],
        "Original url": str,
        "Direct photo url": str,
    },
    total=False,
)


class PhotoPage:
    """Creates an object which stores basic details of a photo and the photo itself"""

    def __init__(self, url: str):
        self.basic_info_dict: PhotoInfo = {}

        if isValid(url):
            # Get name and id of photo
            id_name = url.split("/")[-1].split("-")
            self.basic_info_dict["Id"] = id_name[0]
            self.basic_info_dict["Name"] = " ".join(id_name[1:])

            # Get soup. Can be slow due to internet speeds
            response = get(url)
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            heading = cast(bs4.Tag, soup.find("h1", attrs={"id": "media-title"}))
            meme = heading.a.text.strip() if heading.a else ""
            meme_url = urljoin(KYM, str(heading.a["href"])) if heading.a else ""
            self.basic_info_dict["Meme"] = meme
            self.basic_info_dict["Meme url"] = meme_url
            self.basic_info_dict["Title"] = heading.text.replace(meme, "", 1).strip().removeprefix("-").strip()

            dl_entry = cast(bs4.Tag, soup.find("p", attrs={"id": "tag_list"})).find_all("a", attrs={"data-tag": True})
            self.basic_info_dict["Tags"] = [ele["data-tag"] for ele in dl_entry]

            timeago = cast(bs4.Tag, soup.find("abbr", attrs={"class": "timeago"}))
            if timeago and timeago["title"]:
                self.basic_info_dict["Uploaded"] = parse(str(timeago["title"])).year

            # Store Photo url
            self.basic_info_dict["Original url"] = url

            # Get direct url of photo
            try:
                photo = cast(bs4.Tag, soup.find("textarea", attrs={"class": "photo_embed"}))
                photourl = photo.text.replace(" ", "").replace("!", "")
                self.basic_info_dict["Direct photo url"] = photourl
            except AttributeError:
                print(f"No direct url for was found for {url}")
        else:
            print(f"{url} is not a valid photo url")

    def pprint(self):
        # type: () -> None
        """Pretty print of basic_info_dict"""

        print(dumps(self.basic_info_dict, indent=3))

    def save_json(self, custom_path=DEFAULT_DOWNLOAD_PATH):
        photo_path = os.path.join(custom_path, self.basic_info_dict["Id"] + ".json")

        with open(photo_path, "w", encoding="utf-8") as f:
            f.write(dumps(self.basic_info_dict, indent=2))

    def download_photo(self, custom_path=DEFAULT_DOWNLOAD_PATH):
        # type: (str) -> None
        """Download photo from given url custom_path/Photo name
        If no name is available, the photo is named after its ID instead
        """

        if "Direct photo url" in self.basic_info_dict:
            url = self.basic_info_dict["Direct photo url"]
            response = get(url)
            if response.status_code == 200:
                _, ext = os.path.splitext(parse_url(url).path or "")
                ext = ext or "." + response.headers["Content-Type"].split("/")[-1]

                photo_path = os.path.join(custom_path, self.basic_info_dict["Id"] + ext)

                with open(photo_path, "wb") as f:
                    f.write(response.content)
        else:
            print("Direct photo url is missing or invalid", dumps(self.basic_info_dict))


if __name__ == "__main__":
    ur = "https://knowyourmeme.com/photos/1891689-uzaki-chan-wants-to-hang-out"
    UzakiTsuki = PhotoPage(ur)
    UzakiTsuki.pprint()
    # UzakiTsuki.download_photo()
