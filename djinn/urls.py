from django.contrib import admin
from django.urls import path, include
from djinn import azure_blob


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('inc_mgmt.urls', namespace='inc_mgmt')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('ajax/return_final_url_to_ajax_get/', azure_blob.return_final_url_to_ajax_get, name='return_final_url_to_ajax_get'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
