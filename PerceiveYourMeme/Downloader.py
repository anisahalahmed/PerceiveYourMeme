import os
from time import sleep

from .GetKYM import get_memes
from .MemePage import MemePage
from .PhotoPage import PhotoPage

meme_folder = "data/memes"
os.makedirs(meme_folder, exist_ok=True)
image_folder = "data/images"
os.makedirs(image_folder, exist_ok=True)

processed_file_name = "data/urls.txt"
processed: set[str] = set()
if os.path.exists(processed_file_name):
    with open(processed_file_name) as file:
        for line in file:
            processed.add(line.strip())

download_count = 1
memes_downloaded = 0
page_index = 1
memes = ["memes"]
while memes and memes_downloaded < download_count:
    memes = get_memes(page_index=page_index)
    page_index = page_index + 1
    for meme_url in memes:
        if meme_url in processed:
            continue
        print(meme_url)
        page = MemePage(meme_url)
        page.download_header_image(meme_folder)
        page.save_json(meme_folder)
        sleep(0.5)

        article_images = [item for items in page.basic_info_dict["Body photos"].values() for item in items]
        for image_url in article_images + page.photos("favorites"):
            if image_url in processed:
                continue
            print(image_url)
            image = PhotoPage(image_url)
            image.download_photo(image_folder)
            image.save_json(image_folder)
            processed.add(image_url)
            sleep(0.5)

        processed.add(meme_url)
        memes_downloaded = memes_downloaded + 1
        if memes_downloaded >= download_count:
            break

with open(processed_file_name, "w") as file:
    for line in processed:
        file.write(f"{line}\n")
