from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Userprofile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(MessageModel)
admin.site.register(ThreadModel)