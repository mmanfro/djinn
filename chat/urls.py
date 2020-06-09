from django.urls import path

from chat import views as v


app_name = 'chat'
urlpatterns = [
    path('chat/', v.index, name='index'),
    path('room/<token>/', v.chat_room, name='chat_room'),
    path('ajax/send_file/', v.send_file, name='send_file'),
    path('ajax/create_chat', v.create_chat, name='create_chat'),
    path('ajax/save_chat', v.save_chat, name='save_chat'),
    path('ajax/delete_chat', v.delete_chat, name='delete_chat'),
]