from django.conf.urls.static import static
from . import settings
from django.contrib import admin
from django.urls import path, include
from .views import secure_media
# from 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path("media/<path:path>",secure_media,),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)