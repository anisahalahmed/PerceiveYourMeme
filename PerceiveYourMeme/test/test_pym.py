import os
import unittest

from .. import *

output_folder = "test_outputs"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)


class Test(unittest.TestCase):
    def setUp(self):
        print(self._testMethodName)

    def test_meme_page(self):
        page = MemePage("https://knowyourmeme.com/memes/smudge-the-cat")
        page.pprint()
        page.download_origin_image(output_folder)
        assert "woman yelling at a cat" in page.basic_info_dict["Tags"]

    def test_nsfw_meme(self):
        page = MemePage("https://knowyourmeme.com/memes/events/nashville-covenant-school-shooting")
        page.pprint()
        page.download_origin_image(output_folder)
        assert "covenant school" in page.basic_info_dict["Tags"]
        assert "2023" in page.basic_info_dict["Year"]
        assert page.basic_info_dict["Badge"] == "NSFW"
        assert "Controversy" in page.basic_info_dict["Type"]

    def test_photo_page(self):
        photo = PhotoPage("https://knowyourmeme.com/photos/1894354-nordic-mediterranean")
        photo.pprint()
        photo.download_photo(output_folder)
        assert "adolf hitler" in photo.basic_info_dict["Tags"]
        assert photo.basic_info_dict["Title"] == "Generalplan Ost"

    def test_news_page(self):
        news = NewsPage(
            "https://news.knowyourmeme.com/news/mia-khalifa-is-auctioning-iconic-porn-glasses-to-raise-money-for-beirut"
        )
        assert news.info_dict
        news.pprint()
        news.download_head_img(output_folder)

    def test_video_page(self):
        video = VideoPage("https://knowyourmeme.com/videos/225020-western-animation")
        assert video.basic_info_dict
        video.pprint()

    def test_search_entries(self):
        entries = SearchEntry("Elon Musk")
        entries.search()
        for page in entries.MemePageList:
            for meme in page:
                assert meme.basic_info_dict
                meme.pprint()

    def test_search_images(self):
        images = SearchImage("Elon Musk")
        images.search()
        for page in images.PhotoPageList:
            for photo in page:
                assert photo.basic_info_dict
                photo.pprint()

    def test_search_news(self):
        articles = SearchNews("Elon Musk")
        articles.search()
        for page in articles.NewsPageList:
            for news in page:
                assert news.info_dict
                news.pprint()

    def test_get_memes(self):
        for meme in get_memes():
            assert meme.basic_info_dict
            meme.pprint()

    def test_get_images(self):
        for photo in get_photos():
            assert photo.basic_info_dict
            photo.pprint()

    def test_get_news(self):
        for news in get_news():
            assert news.info_dict
            news.pprint()

    def test_get_images_for_meme(self):
        Smudge = MemePage("https://knowyourmeme.com/memes/smudge-the-cat")
        for page in Smudge.photos():
            for photo in page:
                assert photo.basic_info_dict
                photo.pprint()


if __name__ == "__main__":
    unittest.main()
