from django.shortcuts import render


def chat_room(request, token):
    return render(request, 'inc_mgmt/chat/room.html', {'token': token,})