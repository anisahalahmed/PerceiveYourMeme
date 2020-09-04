import urllib3
import bs4
from CONST import HEADERS, DEFAULT_DOWNLOAD_PATH

class MemePage():
    # An object to store basic information and template of a meme
    def __init__(self, url):
        # Store ulr
        self.url = url

        # Get the html document. This can be slow due to the internet
        http = urllib3.PoolManager()
        response = http.request('GET', url, headers=HEADERS)
        entry_body = bs4.BeautifulSoup(response.data, 'html.parser').find('div', attrs={"class": "c", "id": "entry_body"})

        # Get basic information and entry tags from entry body
        basic_info = [ele for ele in entry_body.find('dl').text.split('\n') if ele != '']
        basic_info_dict = {'Unit':basic_info[0], 'Status':basic_info[2], 'Type':basic_info[4],
                            'Year':basic_info[6]}

        entry_tags = [ele for ele in
                    entry_body.find('dl', attrs={"id":"entry_tags"}).text.split('\n') if ele != '']

        basic_info_dict['Tags'] = entry_tags[1]

        # Name meme
        basic_info_dict['Name'] = url.split('/')[-1]

        # Store basic information
        self.basic_info_dict = basic_info_dict

        # Get url of template
        self.org_img_urls = [ele['data-src'] for ele in entry_body.find('center').find_all('img')]


    def pprint_basic_info(self):
        # Pretty print of basic information
        from json import dumps
        print(dumps(self.basic_info_dict, indent=3))

    def download_origin_image(self, custom_path = DEFAULT_DOWNLOAD_PATH):
        # Download images
        # then name them corresponding to self.basic_info_dict['Name']
        http = urllib3.PoolManager()
        i = 0
        for org_img_url in self.org_img_urls:
            response



if __name__ == '__main__':
    crying_cat = MemePage('https://knowyourmeme.com/memes/crying-cat')
    print(crying_cat.url)
    crying_cat.pprint_basic_info()
    print(crying_cat.org_img_urls)