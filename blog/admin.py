from django.contrib import admin

from blog.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date',)
    search_fields = ('title', 'content',)
    list_filter = ('creation_date',)
