"""
URL configuration for blogchecker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import render
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views_blogs import BlogViewSet

router = DefaultRouter()
router.register(r"blogs", BlogViewSet)


def app(request):
    print("app", request.user)
    return render(request, "web/app.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    re_path(r"^(?!admin/|auth|callback|logout|api/).*", app, name="app"),
]
