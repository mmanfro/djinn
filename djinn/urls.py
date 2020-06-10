from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('inc_mgmt.urls', namespace='inc_mgmt')),
    path('chat/', include('chat.urls', namespace='chat')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
