import asyncio
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
import csv
from tracker.utils import *
from tracker.models import *
from tracker.tasks import *

@api_view(['GET'])
def trigger_report(request):
    # Create a new report status object
    report_obj = ReportStatus.objects.create()
    report_id = report_obj.id

    # Trigger the report generation task asynchronously with Celery
    generate_report_task.delay(report_id)

    # Return response immediately
    return JsonResponse({"status": "report_generation_started", "report_id": report_obj.id})

@api_view(["GET"])
def get_report(request, report_id):

    if not ReportStatus.objects.filter(id=report_id).exists():
        return JsonResponse({"status": "No report found with this id"})
    
    if ReportStatus.objects.get(id=report_id).status == 0:
        return JsonResponse({'status': "processing"})
    
    else:
        return JsonResponse({'status': 'completed'})
    
@api_view(['GET'])
def download_report(request, report_id):
    
    if not ReportStatus.objects.filter(id=report_id).exists():
        return JsonResponse({"status": "No report found with this id"})
    
    queryset = Report.objects.filter(report_id=report_id)
    response = HttpResponse()
    response['mimetype'] = 'text/csv'
    response['Content-Disposition'] = f'attachment;filename=Report-{report_id}.csv'
    writer = csv.writer(response)
    writer.writerow(['store_id', 'uptime_last_hour(in mins)', 'uptime_last_day(in hrs)', 'uptime_last_week(in hrs)',
                        'downtime_last_hour(in mins)', 'downtime_last_day(in hrs)', 'downtime_last_week(in hrs)'])
    for data in queryset:
        writer.writerow([data.store_id, data.uptime_last_hour, data.uptime_last_day, data.uptime_last_week,
                            data.downtime_last_hour, data.downtime_last_day, data.downtime_last_week])
    return response


