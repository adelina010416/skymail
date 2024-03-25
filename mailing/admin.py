from django.contrib import admin

from mailing.models import Mail


# Register your models here.
@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('name', 'status',)
