from django.urls import path
from tracker.views import *

urlpatterns = [
    path('trigger-report', trigger_report, name="trigger-report"),
    path('get-report-status/<int:report_id>', get_report, name="get report"),
    path('get-report/<int:report_id>', download_report, name="download_report")
]