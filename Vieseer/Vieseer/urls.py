"""
URL configuration for Vieseer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from Vieseer import settings
from django.conf.urls.static import static
from VieseerApp.views import register_view,login_view,logout_view,upload_image, gallery, \
    download_image,create_collection,manage_collection,user_collections,like_image,add_to_collection,image_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('upload/', upload_image, name='upload'),
    path('',gallery, name = 'gallery'),
    path('download/<int:image_id>/', download_image, name='download'),
    path('collections/create/', create_collection, name='create_collection'),
    path('collections/manage/<int:image_id>/', manage_collection, name='manage_collection'),
    path('collections/', user_collections, name='user_collections'),
    path('like/<int:image_id>/', like_image, name='like_image'),
    path('add_to_collection/', add_to_collection, name='add_to_collection'),
    path('image/<int:image_id>/', image_detail, name='image_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
