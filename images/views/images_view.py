from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from images.serializers import ImageListSerializer, ImageMetadataListSerializer
from images.services import ImageService


class ImageSearchAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ImageListSerializer
    service_class = ImageService

    def list(self, request: Request, *args, **kwargs) -> Response:
        query_params_dict = request.query_params.dict()
        image_list = self.service_class().image_list(query_params_dict)
        serializer = self.serializer_class(image_list, many=True, context=self.get_serializer_context())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ImageMetadataSearchAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ImageMetadataListSerializer
    service_class = ImageService

    def list(self, request: Request, *args, **kwargs) -> Response:
        query_params_dict = request.query_params.dict()
        image_list = self.service_class().image_metadata_list(query_params_dict)
        serializer = self.serializer_class(image_list, many=True, context=self.get_serializer_context())
        return Response(data=serializer.data, status=status.HTTP_200_OK)
