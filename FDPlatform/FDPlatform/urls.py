from django.contrib import admin
from django.urls import path,include
import django.contrib.auth.urls as auth
from FDPlatform import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(auth), name='authentication'),
    path('', include('FDApp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)