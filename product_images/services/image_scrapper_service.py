from bs4 import BeautifulSoup

import requests
import shutil
import uuid
from io import BytesIO
from PIL import Image


class ImageScrapperService(object):
    def __init__(self, url: str):
        self.url = url
        self.folder = self.get_folder_name()
        self.timeout = 5  # 5 sec

    def get_folder_name(self):
        domain_name = self.url.split("//")[-1].split("/")[0].split('?')[0]
        try:
            folder_name = domain_name.replace(".", "-")
        except:
            folder_name = domain_name
        return folder_name

    def _get_info(self):
        image_list_data = []

        response = requests.get(self.url, timeout=self.timeout)
        beautiful_soup = BeautifulSoup(response.text, "html.parser")
        image_links = beautiful_soup.find_all("img")

        for img in image_links[:3]:
            if img.get("src"):
                # image_list_data.append({"url": img["src"], "alt": img.get("alt", "")})
                image_list_data.append(img["src"])

        return image_list_data

    def _download_images(self, image_data):
        image_url = image_data
        # file_name = image_data["alt"]
        response = requests.get(image_url, stream=True, timeout=self.timeout)
        if response.status_code == 200:
            file_name = image_url.split("/")[-1]
            image_file = BytesIO()
            image_file.write(response.content)
            image_file.name = file_name

    def scrape_images(self):
        image_data = self._get_info()

        for i in range(0, len(image_data)):
            if image_data[i]:
                self._download_images(image_data[i])
