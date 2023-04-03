import os
import unittest
from itertools import islice

from .. import *

output_folder = "test_outputs"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)


class Test(unittest.TestCase):
    def setUp(self) -> None:
        print(self._testMethodName)

    def test_meme_page(self) -> None:
        page = MemePage("https://knowyourmeme.com/memes/smudge-the-cat")
        page.pprint()
        page.download_origin_image(output_folder)
        assert "woman yelling at a cat" in page.basic_info_dict["Tags"]

    def test_nsfw_meme(self) -> None:
        page = MemePage("https://knowyourmeme.com/memes/events/nashville-covenant-school-shooting")
        page.pprint()
        page.download_origin_image(output_folder)
        assert "covenant school" in page.basic_info_dict["Tags"]
        assert "2023" in page.basic_info_dict["Year"]
        assert page.basic_info_dict["Badge"] == "NSFW"
        assert "Controversy" in page.basic_info_dict["Type"]

    def test_photo_page(self) -> None:
        photo = PhotoPage("https://knowyourmeme.com/photos/1894354-nordic-mediterranean")
        photo.pprint()
        photo.download_photo(output_folder)
        assert "adolf hitler" in photo.basic_info_dict["Tags"]
        assert photo.basic_info_dict["Title"] == "Generalplan Ost"

    def test_news_page(self) -> None:
        news = NewsPage(
            "https://news.knowyourmeme.com/news/mia-khalifa-is-auctioning-iconic-porn-glasses-to-raise-money-for-beirut"
        )
        assert news.info_dict
        news.pprint()
        news.download_head_img(output_folder)

    def test_video_page(self) -> None:
        video = VideoPage("https://knowyourmeme.com/videos/225020-western-animation")
        assert video.basic_info_dict
        video.pprint()

    def test_search_entries(self) -> None:
        entries = SearchEntry("Elon Musk")
        for page in entries.search():
            for meme in islice(page, 3):
                assert meme.basic_info_dict
                meme.pprint()

    def test_search_images(self) -> None:
        images = SearchImage("Elon Musk")
        for page in images.search():
            for photo in islice(page, 3):
                assert photo.basic_info_dict
                photo.pprint()

    def test_search_news(self) -> None:
        articles = SearchNews("Elon Musk")
        for page in articles.search():
            for news in islice(page, 3):
                assert news.info_dict
                news.pprint()

    def test_get_memes(self) -> None:
        for meme in map(MemePage, get_memes()[:3]):
            assert meme.basic_info_dict
            meme.pprint()

    def test_get_images(self) -> None:
        for photo in map(PhotoPage, get_photos()[:3]):
            assert photo.basic_info_dict
            photo.pprint()

    def test_get_news(self) -> None:
        for news in map(NewsPage, get_news()[:3]):
            assert news.info_dict
            news.pprint()

    def test_get_images_for_meme(self) -> None:
        meme = MemePage("https://knowyourmeme.com/memes/smudge-the-cat")
        for photo in map(PhotoPage, meme.photos()[:3]):
            assert photo.basic_info_dict
            photo.pprint()


if __name__ == "__main__":
    unittest.main()
