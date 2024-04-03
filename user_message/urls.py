from django.urls import path

from user_message.apps import UserMessageConfig
from user_message.views import *

app_name = UserMessageConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='all_messages'),
    path('create', MessageCreateView.as_view(), name='new_message'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message'),
    path('edit-message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
]
