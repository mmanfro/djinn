from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.http.response import JsonResponse
import ntpath
from chat.models import ChatRoom
from inc_mgmt.views import chat_index
import os


def index(request):
    return chat_index(request)

def chat_room(request, token):
    get_object_or_404(ChatRoom.objects.all().filter(token=token, is_active=True))
    return render(request, 'chat/room.html', {'token': token,})

def send_file(request):
    data = {'sent': False,}
    file = request.FILES['file']
    if file.size > 2621440:
        file = None
    else:
        token = request.POST.get('token')
        path = default_storage.save('chat/' + token + '/' + file.name, file) 
        file_url = default_storage.url(path)
        file_name = ntpath.basename(path)
        
        data = {'file_url': file_url,
                'file_name': file_name,
                'sent': True,}
    
    return JsonResponse(data)

def save_chat(request):
    content = request.POST.get('content')
    token = request.POST.get('token')
    chatroom = ChatRoom.objects.all().filter(token=token)[0]
    with open('content.html', 'w+') as output:
        output.write(str(content))
        chatroom.content.save('content.html', output, save=False)
    os.remove(output.name)
    chatroom.is_active = False
    chatroom.save()
    
    return JsonResponse({})
    