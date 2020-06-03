from django.urls import path

from chat import views as v

urlpatterns = [
    path('room/<token>/', v.chat_room, name='chat_room'),
]