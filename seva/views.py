import datetime
from django.shortcuts import render
from django.utils import timezone
from seva.models import DailySeva
from notifications.services import send_seva_assigned_notification

def generate_daily_sevas_and_notify(assignment, leader_name="Temple Leader"):
    """
    Immediately generates the DailySeva records for the given assignment date range,
    and sends the assignment notification email to the devotee.
    """
    current_date = assignment.start_date
    end_date = assignment.end_date
    
    while current_date <= end_date:
        exists = DailySeva.objects.filter(
            weekly_service=assignment,
            devotee=assignment.devotee,
            seva_date=current_date
        ).exists()
        
        if not exists:
            naive_dt = timezone.datetime.combine(current_date, assignment.start_time)
            start_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
            
            daily_seva = DailySeva.objects.create(
                weekly_service=assignment,
                devotee=assignment.devotee,
                service_name=assignment.service_name,
                seva_date=current_date,
                service_date=current_date,
                start_datetime=start_dt,
                service_start_time=assignment.start_time,
                duration_minutes=assignment.duration_minutes,
                completed=False,
                status='pending'
            )
                
        current_date += datetime.timedelta(days=1)
