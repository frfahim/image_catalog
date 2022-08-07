from rest_framework import serializers
from product_images.models import Images
from product_images.services import ImageService

# defining a random image sizes, we need to define a proper size for real life usages
IMAGE_SIZES = {
    "small": (256, 256),
    "medium": (1024, 1024),
    "large": (2048, 2048)
}


class ImageListSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()

    class Meta:
        model = Images
        fields = [
            "id",
            "media",
            "size",
        ]

    def get_media(self, instance):
        media_url = instance.media.url
        request = self.context["request"]
        if request.query_params.get("size"):
            image_size = IMAGE_SIZES.get(request.query_params["size"])
            if image_size:
                resized_image = ImageService().get_resized_image(
                    image_file=instance.media, width=image_size[0], height=image_size[1]
                )
                media_url = resized_image if resized_image else media_url
        return request.build_absolute_uri(media_url)


class ImageMetadataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            "id",
            "media",
            "size",
            "height",
            "width",
            "created_at",
            "original_url",
        ]
