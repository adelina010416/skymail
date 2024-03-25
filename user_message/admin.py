from django.contrib import admin

from user_message.models import Message


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('header',)
