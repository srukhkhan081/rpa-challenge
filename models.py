import re
import urllib

from utils import convert_string_to_date_time, IMAGE_PATH
from RPA.HTTP import HTTP


class News:
    def __init__(self, title: str, time_stamp: str, img_url: str, description: str = ''):
        self.title = title
        self.time_stamp = convert_string_to_date_time(time_stamp)
        self.img_url = img_url
        self.file_name = self.get_file_name()
        self.description = description
        self.save_image()

    def get_file_name(self):
        if 'url=' in self.img_url.split('/')[-1]:
            url = self.img_url.split('/')[-1].split('url=')[-1]
            decoded_url = urllib.parse.unquote(url)
            return decoded_url.split('/')[-1]
        else:
            return self.img_url.split('/')[-1]

    def search_phrase_count(self, search_phrase: str):
        return self.title.count(search_phrase) + self.description.count(search_phrase)

    def save_image(self):
        downloader = HTTP()
        downloader.download(self.img_url, IMAGE_PATH + self.file_name)

    def check_if_contains_amount(self):
        patterns = [
            r'\$\d+(\.\d+)?',  # $11.1 or $111,111.11
            r'\d+(\.\d+)? dollars',  # 11 dollars
            r'\d+(\.\d+)? USD'  # 11 USD
        ]
        text = self.title + self.description
        for pattern in patterns:
            if re.search(pattern, text):
                return True
        return False
