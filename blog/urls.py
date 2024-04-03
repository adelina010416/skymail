from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import *
from blog.apps import BlogConfig


app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(PostListView.as_view()), name='posts'),
    path('post/<int:pk>', cache_page(60)(PostDetailView.as_view()), name='post'),
]
