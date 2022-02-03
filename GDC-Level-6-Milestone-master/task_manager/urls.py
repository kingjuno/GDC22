from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add all your views here
    path("", include("tasks.urls")),
]
