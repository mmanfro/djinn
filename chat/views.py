from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage
from django.http.response import JsonResponse
import ntpath
from chat.models import ChatRoom
import os
from django.contrib.auth.decorators import login_required
import shutil
from pathlib import Path
from django.utils import timezone
from random import randint
import secrets


def index(request):
    chat_list = ChatRoom.objects.all().filter(created_by=request.user).order_by('-time_created')
    context = {'chat_list': chat_list}
    
    return render(request, 'inc_mgmt/chat/index.html', context)

def chat_room(request, token):
    get_object_or_404(ChatRoom.objects.all().filter(token=token, is_active=True))
    return render(request, 'chat/room.html', {'token': token,})

@login_required
def create_chat(request):
    if request.method == "POST":
        name = request.POST.get('chat_name')
        created_by = request.user
        token = str(int(timezone.now().hour) + int(timezone.now().minute) + (int(timezone.now().second) * randint(1,9))) + (str(secrets.token_urlsafe(1))).replace('_', 'M').upper() 
        token += str(request.user.id) + str(int(timezone.now().day) + (int(timezone.now().second) * randint(1,9))) + (str(secrets.token_urlsafe(1))).replace('_', 'A').upper()
        token.replace('-', 'U')
        chat = ChatRoom(name=name, created_by=created_by, token=token)
        chat.save()
        
    return JsonResponse({})

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

@login_required
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

@login_required
def delete_chat(request):
    if request.method == "POST":
        chat = ChatRoom.objects.all().filter(pk=request.POST.get('chat_id'))[0]
        if chat.content:
            path = Path(chat.content.path)
            shutil.rmtree(path.parent, ignore_errors=True)
        chat.delete()
        
    return JsonResponse({})
    