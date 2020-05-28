from django.contrib import admin
from inc_mgmt.models import User, Area, Status, Priority
from djinn.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Area)
admin.site.register(Priority)
admin.site.register(Status)