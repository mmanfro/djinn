from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url



urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('inc_mgmt.urls', namespace='inc_mgmt')),
    path('chat/', include('chat.urls', namespace='chat')),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
