import unittest
from .. import *


class Test(unittest.TestCase):
    def setUp(self):
        print(self._testMethodName)

    def test_meme_page(self):
        Smudge = MemePage("https://knowyourmeme.com/memes/smudge-the-cat")
        assert Smudge.basic_info_dict
        Smudge.pprint()
        Smudge.download_origin_image()

    def test_image_page(self):
        OneRace = PhotoPage("https://knowyourmeme.com/photos/1894354-nordic-mediterranean")
        assert OneRace.basic_info_dict
        OneRace.pprint()
        OneRace.download_photo()

    def test_news_page(self):
        Mia = NewsPage(
            "https://news.knowyourmeme.com/news/mia-khalifa-is-auctioning-iconic-porn-glasses-to-raise-money-for-beirut"
        )
        assert Mia.info_dict
        Mia.pprint()
        Mia.download_head_img()

    def test_video_page(self):
        western_animation = VideoPage("https://knowyourmeme.com/videos/225020-western-animation")
        assert western_animation.basic_info_dict
        western_animation.pprint()

    def test_search_entries(self):
        ElonMuskEntries = SearchEntry("Elon Musk")
        ElonMuskEntries.search()
        for page in ElonMuskEntries.MemePageList:
            for meme in page:
                assert meme.basic_info_dict
                meme.pprint()

    def test_search_images(self):
        ElonMuskImages = SearchImage("Elon Musk")
        ElonMuskImages.search()
        for page in ElonMuskImages.PhotoPageList:
            for photo in page:
                assert photo.basic_info_dict
                photo.pprint()

    def test_search_news(self):
        ElonMuskNews = SearchNews("Elon Musk")
        ElonMuskNews.search()
        for page in ElonMuskNews.NewsPageList:
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
