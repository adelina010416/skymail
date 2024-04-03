from django.urls import path
from attempt_report.views import *
from attempt_report.apps import AttemptReportConfig

app_name = AttemptReportConfig.name

urlpatterns = [
    path('', AttemptListView.as_view(), name='reports'),
    path('delete/<int:pk>', AttemptDeleteView.as_view(), name='delete_report'),
]
