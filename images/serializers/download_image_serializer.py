from rest_framework import serializers


class DownloadImageSerializer(serializers.Serializer):
    web_url = serializers.URLField()
