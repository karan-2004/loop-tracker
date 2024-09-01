# your_app/tasks.py

from celery import shared_task
from tracker.utils import generate_report

@shared_task
def generate_report_task(report_id):
    # Your existing synchronous generate_report function
    generate_report(report_id)
