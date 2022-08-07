from product_images.models import Images
from django.core.files.images import ImageFile


class ImageService(object):
    model = Images

    def map_image_data(self, image_object, url):
        """
        Map media data for image
        will be used for scrape image from external source
        """
        try:
            image = ImageFile(image_object, image_object.name)
            media_data = {
                "media": image,
                "size": image.size / 1024,  # in KB
                "width": image.width,
                "height": image.height,
                "original_url": url
            }
            return media_data
        except Exception as e:
            # We can log the exception for further investigate or raise an error
            print(e)

    def save_image(self, image_object, url):
        image_data = self.map_image_data(image_object, url)
        try:
            image_instance = self.model.objects.create(**image_data)
        except Exception as exp:
            # log this exception
            image_instance = None
            print("Couldn't save image")
        return image_instance

    def image_list(self, query_params):
        images = self.model.objects.all()
        if query_params.get("id"):
            images = images.filter(id=query_params["id"])
        if query_params.get("url"):
            images = images.filter(orginal_url__contains=query_params["url"])
        if query_params.get("size"):
            pass
        return images

    def image_metadata_list(self, query_params):
        images = self.model.objects.all()
        if query_params.get("id"):
            images = images.filter(id=query_params["id"])
        if query_params.get("url"):
            images = images.filter(orginal_url__contains=query_params["url"])
        return images

