import datetime
import os.path
import logging

from dateutil import parser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def convert_string_to_date_time(datetime_string):
    """
    Convert a string representation of datetime to a datetime object.

    Args:
        datetime_string (str): The string representation of datetime.

    Returns:
        datetime.datetime: The datetime object.
    """
    if "ago" not in datetime_string:
        return parser.parse(datetime_string)
    else:
        if 'minutes' in datetime_string:
            return datetime.datetime.now() - datetime.timedelta(minutes=int(datetime_string.split('minutes')[0].strip()))
        elif 'hours' in datetime_string:
            return datetime.datetime.now() - datetime.timedelta(hours=int(datetime_string.split('hours')[0].strip()))
        else:
            return datetime.datetime.now()


def create_path_if_not_exists(path):
    """
    Create a directory if it doesn't exist.

    Args:
        path (str): The path of the directory to be created.
    """
    if not os.path.exists(path):
        os.makedirs(path)


OUTPUT_PATH = f"{os.getcwd()}/output/"
IMAGE_PATH = f"{os.getcwd()}/images/"

create_path_if_not_exists(OUTPUT_PATH)
create_path_if_not_exists(IMAGE_PATH)
