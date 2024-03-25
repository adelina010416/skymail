from django.urls import path
from blog.views import *
from blog.apps import BlogConfig


app_name = BlogConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='posts')
]