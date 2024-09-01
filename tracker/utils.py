from datetime import datetime, timedelta, date
import pytz
from django.db.models import Sum, Case, When, IntegerField, Max, F, OuterRef, Subquery
from django.db.models.functions import ExtractWeekDay
from asgiref.sync import sync_to_async
from tracker.models import *

# Query to get uptime and downtime for the last hour, day, and week
def calculate_uptime_downtime(store_id):
    # Define time intervals
    now = StoreStatus.objects.aggregate(curr_time=Max('timestamp_utc'))['curr_time']
    last_hour = now - timedelta(hours=1)
    last_day = now - timedelta(days=1)
    last_week = now - timedelta(weeks=1)

    poll_data = StoreStatus.objects.filter(store_id=store_id, timestamp_utc__gte=last_week)
    for data in poll_data:
        print(data.timestamp_utc.weekday(), data.timestamp_utc)

    # Get the timezone of the store
    tz = Timezone.objects.get(store_id=store_id).timezone_str
    local_tz = pytz.timezone(tz)

    # Convert UTC times to local times
    last_hour_local = last_hour.astimezone(local_tz)
    last_day_local = last_day.astimezone(local_tz)
    last_week_local = last_week.astimezone(local_tz)

    # Filter poll data within business hours

    uptime_downtime = {}

    
    # Example timezone conversion function
    def convert_time_to_utc(local_time, local_tz):
        today = date.today()
        naive_datetime = datetime.combine(today, local_time)
        local_datetime = local_tz.localize(naive_datetime)
        utc_datetime = local_datetime.astimezone(pytz.UTC)
        return utc_datetime.time()
    
    business_hour_dict = {}

    business_hours_of_a_store = BusinessHour.objects.filter(store_id=store_id)

    for business_hour in business_hours_of_a_store:
        business_hour_dict[business_hour.day] = {
            'start_time': business_hour.start_time_local,
            'end_time': business_hour.end_time_local,
            'start_time_utc': convert_time_to_utc(business_hour.start_time_local, local_tz),
            'end_time_utc': convert_time_to_utc(business_hour.end_time_local, local_tz) 
        }

    print(business_hour_dict)

    for period, start_time in [('hour', last_hour_local), ('day', last_day_local), ('week', last_week_local)]:
        poll_data = poll_data.filter(timestamp_utc__gte=start_time.astimezone(pytz.UTC))
        filtered_data = poll_data.annotate(
            weekday=ExtractWeekDay('timestamp_utc'),
            within_business_hours=Case(
                *[When(
                weekday=day,
                timestamp_utc__time__gte=business_hour_dict[day]['start_time_utc'],
                timestamp_utc__time__lte=business_hour_dict[day]['end_time_utc'],
                then=1
            ) for day in business_hour_dict.keys()],
            default=0,
            output_field=IntegerField()
            )
        ).filter(within_business_hours=1)

        print(filtered_data)

        # Calculate uptime and downtime
        uptime_minutes = poll_data.filter(status="active").count() * 60 # Each poll represents 1 minute
        downtime_minutes = poll_data.filter(status="inactive").count() * 60

        uptime_downtime[f'uptime_last_{period}'] = uptime_minutes // 60 if period != 'hour' else uptime_minutes
        uptime_downtime[f'downtime_last_{period}'] = downtime_minutes // 60 if period != 'hour' else downtime_minutes

    return uptime_downtime


def generate_report(report_id):
    # Fetch the stores queryset and convert it to a list asynchronously
    stores = Timezone.objects.all()
    report_obj = ReportStatus.objects.get(id=report_id)

    # Iterate over the list of stores
    for ind, store in enumerate(stores[:10]):
        store_id = store.store_id
        report_dict = calculate_uptime_downtime(store_id)
        print(report_dict)
        Report.objects.create(store_id=store_id, report_id=report_obj, **report_dict)
        print(ind)

    # Update the report status
    report_obj.status = 1
    report_obj.save()