from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('inc_mgmt.urls', namespace='inc_mgmt')),
    path('chat/', include('chat.urls')),
]
