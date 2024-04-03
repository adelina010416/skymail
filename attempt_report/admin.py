from django.contrib import admin

from attempt_report.models import Attempt


# Register your models here.
@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('mail', 'user', 'date_time', 'status',)
    search_fields = ('mail', 'user', 'status',)
    list_filter = ('mail', 'user', 'status',)
