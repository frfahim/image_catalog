from django.urls import path, include

from product_images.views import *


app_name = "images"
urlpatterns = [
    path(
        "download/",
        DownloadImageAPIView.as_view(),
        name="tweet-create"
    ),
    path(
        "search/",
        ImageSearchAPIView.as_view(),
        name="tweet-create"
    ),
    path(
        "metadata/search/",
        ImageMetadataSearchAPIView.as_view(),
        name="tweet-create"
    ),
]
