import argparse
import os
import shutil
import signal
from time import time

from .GetKYM import get_memes
from .MemePage import MemePage
from .PhotoPage import PhotoPage
from .CONST import KYM

parser = argparse.ArgumentParser(description="Download all memes")
parser.add_argument(
    "-c",
    "--category",
    help="'meme' or 'culture' or 'subculture' or 'event' or 'person' or 'site' (default all)",
)
parser.add_argument(
    "-d",
    "--directory",
    default="confirmed",
    help="'confirmed' or 'submissions' or 'researching' or 'newsworthy' or 'popular'  or 'deadpool' or 'all' (default 'confirmed'). availability may depend on category",
)
parser.add_argument(
    "-s",
    "--sort",
    default="newest",
    help="'newest' or 'oldest' or 'views' or 'comments' or 'chronological' or 'reverse-chronological' or 'images' or 'videos' (default 'newest')",
)
parser.add_argument(
    "-n",
    "--count",
    default="1",
    help="the number of memes to download (default 1)",
)
parser.add_argument(
    "-p",
    "--page",
    default="1",
    help="start from this page of results (default 1)",
)
parser.add_argument(
    "-o",
    "--output",
    default="data",
    help="the output directory (default ./data)",
)
parser.add_argument(
    "-a",
    "--article-images",
    const=True,
    action="store_const",
    help="download images shown in meme article text",
)
parser.add_argument(
    "-i",
    "--images",
    help="download first page of related images for each meme, sorted by 'newest' or 'oldest' or 'comments' or 'favorites' or 'score' or 'low-score' or 'views'",
)
parser.add_argument(
    "-f",
    "--free",
    help="cancel download if free space passes this limit (in gb). checked after each page",
)
parser.add_argument(
    "--free-path",
    help="override the file path to check free space at (otherwise uses the output folder)",
)

args = parser.parse_args()

print(
    "downloading up to",
    args.count,
    args.directory,
    f"{args.category} entries," if args.category else "entries of any type,",
    "starting from page",
    args.page,
)

meme_folder = os.path.join(args.output, "memes")
os.makedirs(meme_folder, exist_ok=True)
image_folder = os.path.join(args.output, "images")
os.makedirs(image_folder, exist_ok=True)

processed_file_name = os.path.join(args.output, "urls.txt")
processed: set[str] = set()
if os.path.exists(processed_file_name):
    with open(processed_file_name) as file:
        for line in file:
            processed.add(line.strip())


def save_processed(url: str):
    processed.add(url)
    with open(processed_file_name, "a") as file:
        file.write(f"{url}\n")


gb = 1 << 30
start_time = time()


def check_free_space():
    if not args.free:
        return True
    _, used, free = shutil.disk_usage(args.free_path or args.output)
    gb_free = free / gb
    print(round(used / gb, 2), "gb used", round(gb_free, 2), "gb free")
    return gb_free > float(args.free)


def handler(signum, frame):
    exit(1)


signal.signal(signal.SIGINT, handler)

download_count = int(args.count)
memes_downloaded = 0
page_index = int(args.page)
memes = ["memes"]
while memes and memes_downloaded < download_count and check_free_space():
    memes = get_memes(category=args.category, directory=args.directory, page_index=page_index, sort=args.sort)
    print(round(time() - start_time, 1), "seconds: page", page_index)
    for i, meme_url in enumerate(memes):
        if meme_url in processed:
            continue
        page = MemePage(meme_url)
        page.download_header_image(meme_folder)
        page.save_json(meme_folder)
        print(round(time() - start_time, 1), "seconds: meme", f"{i}/{len(memes)}", meme_url)

        article_images = (
            [item for items in page.basic_info_dict["Body photos"].values() for item in items]
            if args.article_images
            else []
        )
        page_photos = page.photos(args.images) if args.images else []
        for image_url in article_images + page_photos:
            canonical_url = KYM + "/photos/" + image_url.split("/")[-1].split("-")[0]
            if canonical_url in processed:
                continue
            image = PhotoPage(image_url)
            dir = os.path.join(image_folder, page.basic_info_dict["Name"])
            os.makedirs(dir, exist_ok=True)
            image.download_photo(dir)
            image.save_json(dir)
            print(round(time() - start_time, 1), "seconds", image_url)
            save_processed(canonical_url)

        save_processed(meme_url)
        memes_downloaded = memes_downloaded + 1
        if memes_downloaded >= download_count:
            break
    page_index = page_index + 1
