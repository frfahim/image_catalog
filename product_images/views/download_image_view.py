
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from product_images.serializers import DownloadImageSerializer


class DownloadImageAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DownloadImageSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response("Images are downloading", status=status.HTTP_200_OK)
