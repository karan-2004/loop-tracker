from django.db import models

# Create your models here.
class StoreStatus(models.Model):
    store_id = models.CharField(max_length=100)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)

class BusinessHour(models.Model):

    store_id = models.CharField(max_length=100)
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class Timezone(models.Model):

    store_id = models.CharField(max_length=100)
    timezone_str = models.CharField(max_length=200)

class ReportStatus(models.Model):
    status = models.BooleanField(default=0)

class Report(models.Model):

    report_id = models.ForeignKey(ReportStatus, on_delete=models.CASCADE)
    store_id = models.CharField(max_length=100)
    uptime_last_hour = models.CharField(max_length=10)
    uptime_last_day = models.CharField(max_length=10)
    uptime_last_week = models.CharField(max_length=10)
    downtime_last_hour = models.CharField(max_length=10)
    downtime_last_day = models.CharField(max_length=10)
    downtime_last_week = models.CharField(max_length=10)