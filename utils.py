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
    if not os.path.exists(path):
        os.makedirs(path)


OUTPUT_PATH = f"{os.getcwd()}/output/"
IMAGE_PATH = f"{OUTPUT_PATH}/images/"

create_path_if_not_exists(OUTPUT_PATH)
create_path_if_not_exists(IMAGE_PATH)
