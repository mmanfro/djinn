from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from inc_mgmt.models import User
import os

def get_upload_path(instance, filename):
    path = ""
    folder = ""
    if isinstance(instance, ChatRoom):
        folder = instance.token
        path = "chat/"
    
    return os.path.join(path + str(folder) + "/" + filename)

class ChatRoom(models.Model):
    name = models.CharField(_('name'), max_length=30)
    # The content is saved in a .html file inside a folder created specific for each chat room along with the sent files
    content = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    # The token is randomly generated and is the key to enter the room
    token  = models.CharField(_('token'), max_length=64, editable=False, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)
    time_created = models.DateTimeField(_('creation time'), default=timezone.now, editable=False)
    is_active = models.BooleanField(_('active'), default=True)