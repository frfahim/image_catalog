"""image_catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Image Catalog API Endpoints",
        default_version="v1",
        description="API endpoints for Image Catalog backend application",
        terms_of_service="",
        contact=openapi.Contact(email="farhadur.fahim@gmail.com")
    ),
    public=True,
    permission_classes=[AllowAny],
)


api_patterns = ([
    path(
        f"docs/",
        schema_view.with_ui("swagger", cache_timeout=0), name="image-catalog-swagger-ui"
    ),
    path(
        "images/",
        include("images.urls", namespace="images")
    ),
], "api")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(api_patterns, namespace="API_V1")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
