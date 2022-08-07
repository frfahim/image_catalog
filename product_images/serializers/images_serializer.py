from rest_framework import serializers
from product_images.models import Images


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            "id",
            "media",
            "size",
        ]


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
