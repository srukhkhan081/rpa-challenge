import re
import urllib

from utils import convert_string_to_date_time, IMAGE_PATH
from RPA.HTTP import HTTP


class News:
    """
    Class representing a news article.
    """

    def __init__(self, title: str, time_stamp: str, img_url: str, description: str = ''):
        """
        Initialize a News object.

        Args:
            title (str): The title of the news article.
            time_stamp (str): The timestamp of the news article.
            img_url (str): The URL of the image associated with the news article.
            description (str, optional): The description of the news article. Defaults to ''.
        """
        self.title = title
        self.time_stamp = convert_string_to_date_time(time_stamp)
        self.img_url = img_url
        self.file_name = self.get_file_name()
        self.description = description
        self.save_image()
        self.downloader = HTTP()

    def get_file_name(self):
        """
        Extract the file name from the image URL.

        Returns:
            str: The file name.
        """
        if 'url=' in self.img_url.split('/')[-1]:
            url = self.img_url.split('/')[-1].split('url=')[-1]
            decoded_url = urllib.parse.unquote(url)
            return decoded_url.split('/')[-1]
        else:
            return self.img_url.split('/')[-1]

    def search_phrase_count(self, search_phrase: str):
        """
        Count occurrences of a search phrase in the news title and description.

        Args:
            search_phrase (str): The search phrase.

        Returns:
            int: The count of occurrences.
        """
        return self.title.count(search_phrase) + self.description.count(search_phrase)

    def save_image(self):
        """
        Download and save the image associated with the news article.
        """
        self.downloader.download(self.img_url, IMAGE_PATH + self.file_name)

    def check_if_contains_amount(self):
        """
        Check if the news article title or description contains an amount.

        Returns:
            bool: True if an amount is found, False otherwise.
        """
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
