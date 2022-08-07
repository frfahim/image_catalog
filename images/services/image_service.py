import os
from images.models import Images
from django.core.files.images import ImageFile
from django.core.files.storage import get_storage_class
from django.conf import settings
from PIL import Image

storage = get_storage_class()()


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
                "size": image.size,
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
            images = images.filter(original_url__contains=query_params["url"])
        if query_params.get("size"):
            pass
        return images

    def image_metadata_list(self, query_params):
        images = self.model.objects.all()
        if query_params.get("id"):
            images = images.filter(id=query_params["id"])
        if query_params.get("url"):
            images = images.filter(original_url__contains=query_params["url"])
        return images

    @staticmethod
    def _get_resize_image_name(image_file, x_size, y_size):
        """
        Generates name for the resize image. Returns as tuple file name and extention
        """
        # basename = os.path.basename(image_file.name)
        filename, extension = os.path.splitext(image_file.name)
        new_name = f"{filename}_{x_size}x{y_size}"
        return new_name, extension

    @staticmethod
    def _generate_resized_image(original_img_file, pil_image, x_size, y_size):
        """
        Generates new image (`pil_image` is Pillow image object) with size `x_size` and `y_size`.
        """
        img_width = original_img_file.width
        img_height = original_img_file.height

        if x_size > img_width or y_size > img_height:
            return pil_image

        new_dimensions = (x_size, y_size)
        return pil_image.resize(new_dimensions)

    def get_resized_image(self, image_file, width, height):
        # generate resized image name
        new_name, extension = self._get_resize_image_name(image_file, width, height)
        resized_image_name_with_path = f"{new_name}{extension}"

        # check, if resized img already exists. if not, create resized image file
        if not storage.exists(resized_image_name_with_path):
            try:
                image = Image.open(image_file)
            except: # handle exception properly
                return
            image = self._generate_resized_image(
                original_img_file=image_file,
                pil_image=image,
                x_size=width,
                y_size=height
            )
            try:
                image.save(os.path.join(settings.MEDIA_ROOT, resized_image_name_with_path))
                image.close()
            except OSError as exp:
                image = Image.open(image_file)
                image.convert('RGB').save(os.path.join(settings.MEDIA_ROOT, resized_image_name_with_path))
                image.close()
            except Exception as exp:
                return

        image = storage.url(resized_image_name_with_path)
        return image
