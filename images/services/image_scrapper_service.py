import uuid
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from images.services.image_service import ImageService
from rest_framework.exceptions import APIException



class ImageScrapperService(object):
    def __init__(self, url: str):

        self.url = url
        self.folder = self.get_folder_name()
        self.timeout = 5  # 5 sec
        self.image_service = ImageService()

    def get_folder_name(self):
        domain_name = self.url.split("//")[-1].split("/")[0].split('?')[0]
        try:
            folder_name = domain_name.replace(".", "-")
        except: # handle exception explicitly
            folder_name = domain_name
        return folder_name

    def _get_info(self):
        image_list_data = []

        response = requests.get(self.url, timeout=self.timeout)
        if response.status_code == 200:
            beautiful_soup = BeautifulSoup(response.text, "html.parser")
            image_links = beautiful_soup.find_all("img")

            for img in image_links:
                if img.get("src"):
                    image_list_data.append(img["src"])

            return image_list_data
        else:
            raise APIException(code=response.status_code, detail=response.reason)

    def _download_images(self, image_data):
        image_url = image_data
        # file_name = image_data["alt"]
        response = requests.get(image_url, stream=True, timeout=self.timeout)
        if response.status_code == 200:
            # file_name = image_url.split("/")[-1]
            file_name = uuid.uuid4().hex
            image_file = BytesIO()
            image_file.write(response.content)
            image_file.name = f"{self.folder}/{file_name}.jpg"
            self.image_service.save_image(image_file, self.url)

    # TODO: make this task asyncronus
    def scrape_images(self):
        image_data = self._get_info()

        for img in image_data:
            self._download_images(img)
