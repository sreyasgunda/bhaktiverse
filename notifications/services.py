import sys
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification
from django.utils import timezone

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        try:
            sys.stdout.buffer.write((text + "\n").encode('utf-8'))
            sys.stdout.flush()
        except Exception:
            print(text.encode('ascii', errors='replace').decode('ascii'))

def send_seva_assigned_notification(user, seva, leader_name="Temple Leader"):
    subject = "New Service Assigned"
    local_start = timezone.localtime(seva.start_datetime)
    time_str = local_start.strftime('%I:%M %p')
    
    body = f"""You have been assigned the service: {seva.service_name}
Description: Dedicated devotional service in the temple.
Assigned Time: {time_str}
Assigned by: {leader_name}"""
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        safe_print("EMAIL SENT → Daily Seva Assignment")
        Notification.objects.create(user=user, seva_duty=seva, message=subject, type='assignment')
    except Exception as e:
        safe_print(f"EMAIL FAILED: {e}")

def send_seva_30_min_reminder(user, seva):
    subject = "Seva Reminder"
    body = 'Your service starts in 30 minutes.'
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        safe_print("EMAIL SENT → 30 min reminder")
        Notification.objects.create(user=user, seva_duty=seva, message=body, type='reminder_30')
    except Exception as e:
        safe_print(f"EMAIL FAILED: {e}")

def send_seva_10_min_reminder(user, seva):
    subject = "Seva Reminder"
    body = 'Please remember to complete your ongoing service.'
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        safe_print("EMAIL SENT → 10 min reminder")
        Notification.objects.create(user=user, seva_duty=seva, message=body, type='reminder_10')
    except Exception as e:
        safe_print(f"EMAIL FAILED: {e}")

def send_seva_start_reminder(user, seva):
    subject = "Seva Started"
    body = 'Your service time has started.'
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        safe_print("EMAIL SENT → Service start reminder")
        Notification.objects.create(user=user, seva_duty=seva, message=body, type='reminder_start')
    except Exception as e:
        safe_print(f"EMAIL FAILED: {e}")

def send_sadhana_reminder(user):
    subject = "Reminder: Submit Daily Sadhana"
    body = "Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard."
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        safe_print("EMAIL SENT → 8 AM sadhana reminder")
    except Exception as e:
        safe_print(f"EMAIL FAILED: {e}")

def send_seva_completed_notification(user, seva, leader_emails):
    # To devotee
    dev_subject = "Thank you for your service"
    dev_body = "Thank you for your valuable service.\nYour seva has been successfully completed."
    try:
        send_mail(dev_subject, dev_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        Notification.objects.create(user=user, seva_duty=seva, message=dev_subject, type='completed')
    except Exception as e:
        pass

    # To leaders
    if leader_emails:
        lead_subject = f"Seva Completed: {seva.title}"
        lead_body = f"Devotee {user.name} has completed the service '{seva.title}'."
        try:
            send_mail(lead_subject, lead_body, settings.DEFAULT_FROM_EMAIL, leader_emails, fail_silently=False)
        except Exception as e:
            pass

def send_overdue_alert(user, seva, leader_emails):
    if not leader_emails:
        return
    subject = "Service Not Completed"
    body = f"Devotee: {user.name}\nService: {seva.title}\nScheduled Time: {seva.start_time.strftime('%I:%M %p')} - {seva.end_time.strftime('%I:%M %p')}\n\nService not completed on time."
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, leader_emails, fail_silently=False)
    except Exception as e:
        pass

def send_overdue_failure_alert(user, seva, leader_emails):
    if not leader_emails:
        return
    subject = "Service Not Completed"
    body = "Devotee did not complete assigned seva on time."
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, leader_emails, fail_silently=False)
        safe_print("EMAIL SENT → Service not completed alert")
    except Exception as e:
        safe_print(f"EMAIL FAILED: {e}")

def send_inactive_alert(user, days, leader_emails):
    if not leader_emails:
        return
    subject = "Inactive Devotee Alert"
    body = f"Devotee: {user.name}\nInactive for: {days} days\n\nPlease contact and encourage."
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, leader_emails, fail_silently=False)
    except Exception as e:
        pass

def send_sadhana_summary_alert(leader, unsubmitted_names):
    subject = "Devotees who did not submit Sadhana"
    body = "The following devotees have not submitted today's sadhana:\n\n" + "\n".join(unsubmitted_names)
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [leader.email], fail_silently=False)
    except Exception as e:
        pass

