from django.contrib import admin

from djinn.admin import UserAdmin
from inc_mgmt.models import User, Area, Status, Priority


admin.site.register(User, UserAdmin)
admin.site.register(Area)
admin.site.register(Priority)
admin.site.register(Status)