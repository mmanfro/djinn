from django.urls import path

from chat import views as v


app_name = 'chat'
urlpatterns = [
    path('', v.index, name='index'),
    path('room/<token>/', v.chat_room, name='chat_room'),
    path('ajax/send_file/', v.send_file, name='send_file'),
    path('ajax/save_chat', v.save_chat, name='save_chat'),
]