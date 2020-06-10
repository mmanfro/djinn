from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('inc_mgmt.urls', namespace='inc_mgmt')),
    path('chat/', include('chat.urls', namespace='chat')),
    path(settings.MEDIA_URL)
]
