from urllib import error
from urllib.request import urlretrieve
from urllib.error import URLError, HTTPError
import os

ROOT_DIR = os.path.abspath('.') # Get root directory


def read_file(path: str, encode="utf-8"):
    with open(path, "r", encoding=encode) as file:
        return file.read()


def download_file(file_name: str, url: str):
    file_path = os.path.join(ROOT_DIR, file_name)
    try:
        urlretrieve(url, file_path)
        return file_path
    except (URLError, HTTPError) as err:
        print("Error at download_file function. ", str(err))


if __name__ == '__main__':
    download_file('restaurants.csv', 'https://recruiting-datasets.s3.us-east-2.amazonaws.com/restaurantes.csv')