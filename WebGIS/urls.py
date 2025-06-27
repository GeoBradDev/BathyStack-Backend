from django.contrib import admin
from django.urls import path, include
from api.api import api as missions_api
from ninja import NinjaAPI

api = NinjaAPI(title="BathyStack API")

api.add_router("/missions/", missions_api, tags=["missions"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    path("_allauth/", include("allauth.headless.urls")),
]
