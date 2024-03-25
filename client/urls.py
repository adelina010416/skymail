from django.urls import path
from client.views import *
from client.apps import ClientConfig


app_name = ClientConfig.name

urlpatterns = [
    path('my-clients/', ClientListView.as_view(), name='my_clients'),
    path('create-client/', ClientCreateView.as_view(), name='create_client'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('client-edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client-delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
