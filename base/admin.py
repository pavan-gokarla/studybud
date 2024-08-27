from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Room)
class AdminRooms(admin.ModelAdmin):
    list_display=["name","updated","created"]

admin.site.register(Message)


admin.site.register(Topic)