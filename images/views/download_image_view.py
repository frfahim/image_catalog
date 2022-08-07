
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from images.serializers import DownloadImageSerializer
from images.services import ImageScrapperService


class DownloadImageAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DownloadImageSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_scrapper = ImageScrapperService(url=serializer.validated_data["web_url"])
        image_scrapper.scrape_images()

        return Response("Images are downloading", status=status.HTTP_200_OK)
