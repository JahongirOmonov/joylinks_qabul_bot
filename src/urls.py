
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
