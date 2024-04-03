from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import *

app_name = MailingConfig.name

urlpatterns = [
    path('home/', cache_page(60)(home), name='home'),
    path('mails/', cache_page(60)(MailListView.as_view()), name='mails'),
    path('my-mails/', my_mailing, name='my_mails'),
    path('new-mailing', MailCreateView.as_view(), name='new_mailing'),
    path('mail/<int:pk>', MailDetailView.as_view(), name='mail'),
    path('edit-mail/<int:pk>', MailUpdateView.as_view(), name='edit_mail'),
    path('delete/<int:pk>', MailDeleteView.as_view(), name='delete_mail'),
    path('start-mail/<int:pk>', start_mailing, name='start_mailing'),
    path('stop-mail/<int:pk>', stop_mailing, name='stop_mail'),
    path('save-mail/<int:pk>', save_mail, name='save_mail'),
]
