# KYM : Known Your Meme
KYM = "https://knowyourmeme.com"

KYM_HASH = {
    "memes": "https://knowyourmeme.com/memes/",
    "category": "https://knowyourmeme.com/categories/",
    "photos": "https://knowyourmeme.com/photos/page/",
    "news": "https://knowyourmeme.com/news/page/",
}
# KYM_HASH : a set of directories
# append a positive integer to get the corresponding page number
# For example, https://knowyourmeme.com/memes/page/1 will be the page.

MEMES_SORT_HASH = {"views": "?sort=views", "comments": "?sort=comments", "": ""}
# MEMES_SORT_HASH : a set of sorting methods
# append sort method to MEMES_HASH or KYM_HASH['memes'] to get sort
# For example, https://knowyourmeme.com/memes/popular/page/1?sort=views

PHOTOS_HASH = {
    "trending": "https://knowyourmeme.com/photos/trending/page/",
    "most-commented": "https://knowyourmeme.com/photos/most-commented/page/",
}
# PHOTOS_HASH : a set of sub-directories
# append a positive integer to get the corresponding page number
# For example, https://knowyourmeme.com/memes/trending/page/1 will be the page.

# Why don't PHOTOS_HASH have PHOTOS_SORT_HASH likes MEMES_HASH?
# Because KYM developers treat sort just like sub-directories

DEFAULT_DOWNLOAD_PATH = ""
# Define default download path
# This depends on OS
# If you are smart and have time, https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder
