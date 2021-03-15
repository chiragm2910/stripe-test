from django.contrib import admin
from django.urls import include, path

from .views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view()),
    path("", include("registration.urls"), name="registration"),
]
