from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta

from seva.models import WeeklyServiceAssignment, DailySeva
from sadhana.models import SadhanaEntry
from accounts.models import CustomUser
from .models import Notification

from .services import (
    send_seva_assigned_notification,
    send_seva_30_min_reminder,
    send_seva_10_min_reminder,
    send_seva_start_reminder,
    send_sadhana_reminder,
    send_overdue_failure_alert,
    send_inactive_alert,
)


def get_leader_emails(residency):

    return list(
        CustomUser.objects.filter(
            profile__role='leader',
            profile__residency=residency
        ).values_list('email', flat=True)
    )


def scan_seva_duties():

    print("SCHEDULER RUNNING → scan_seva_duties")

    now = timezone.localtime()
    today = now.date()

    # CREATE DAILY SEVAS
    assignments = WeeklyServiceAssignment.objects.filter(
        active=True,
        start_date__lte=today,
        end_date__gte=today
    )

    for assignment in assignments:

        exists = DailySeva.objects.filter(
            weekly_service=assignment,
            devotee=assignment.devotee,
            seva_date=today
        ).exists()

        if not exists:

            naive_dt = timezone.datetime.combine(
                today,
                assignment.start_time
            )

            start_dt = timezone.make_aware(
                naive_dt,
                timezone.get_current_timezone()
            )

            DailySeva.objects.create(
                weekly_service=assignment,
                devotee=assignment.devotee,
                service_name=assignment.service_name,
                seva_date=today,
                service_date=today,
                start_datetime=start_dt,
                service_start_time=assignment.start_time,
                duration_minutes=assignment.duration_minutes,
                completed=False,
                status='pending'
            )

            print(f"DailySeva created → {assignment.service_name}")

    # REMINDER SYSTEM
    pending_sevas = DailySeva.objects.filter(
        status='pending',
        service_date=today
    )

    for seva in pending_sevas:

        if seva.completed:
            continue

        user = seva.devotee

        if not user or not user.email:
            continue

        residency = getattr(
            user.profile,
            'residency',
            'Main Residency'
        )

        leader_emails = get_leader_emails(residency)

        start_dt_local = timezone.localtime(seva.start_datetime)

        end_dt_local = (
            start_dt_local +
            timedelta(minutes=seva.duration_minutes)
        )

        print("========== DEBUG ==========")
        print("NOW TIME :", now)
        print("START TIME :", start_dt_local)
        print("END TIME :", end_dt_local)
        print("SERVICE :", seva.service_name)
        print("===========================")

        # 30 MIN REMINDER
        if (
            now >= start_dt_local - timedelta(minutes=30)
            and now < start_dt_local
        ):

            if not seva.reminder_30_sent:

                send_seva_30_min_reminder(user, seva)

                seva.reminder_30_sent = True
                seva.save()

                print("EMAIL SENT → 30 min reminder")

        # START + 10 MIN REMINDERS
        elif now >= start_dt_local and now < end_dt_local:

            if not seva.reminder_start_sent:

                send_seva_start_reminder(user, seva)

                seva.reminder_start_sent = True
                seva.last_reminder_time = now

                seva.save()

                print("EMAIL SENT → Service start reminder")

            elif now >= start_dt_local + timedelta(minutes=10):

                base_time = (
                    seva.last_reminder_time
                    if seva.last_reminder_time
                    else start_dt_local
                )

                mins = (
                    now - base_time
                ).total_seconds() / 60.0

                if mins >= 10:

                    send_seva_10_min_reminder(user, seva)

                    seva.last_reminder_time = now
                    seva.save()

                    print("EMAIL SENT → 10 min reminder")

        # OVERDUE ALERT
        elif now >= end_dt_local:

            if not seva.overdue_alert_sent:

                send_overdue_failure_alert(
                    user,
                    seva,
                    leader_emails
                )

                seva.overdue_alert_sent = True
                seva.save()

                print("EMAIL SENT → Service not completed alert")

def scan_sadhana_entries():

    now = timezone.localtime()

    hour = now.hour
    minute = now.minute

    # HOURLY REMINDERS
    if 8 <= hour < 12 and minute == 0:

        devotees = CustomUser.objects.filter(
            profile__role='devotee'
        )

        for user in devotees:

            has_sadhana = SadhanaEntry.objects.filter(
                user=user,
                sadhana_date=now.date()
            ).exists()

            if not has_sadhana:

                recent = Notification.objects.filter(
                    user=user,
                    type='sadhana_reminder',
                    created_at__gte=now - timedelta(minutes=45)
                ).exists()

                if not recent:

                    Notification.objects.create(
                        user=user,
                        message="Reminder: Submit Daily Sadhana",
                        type='sadhana_reminder'
                    )

                    send_sadhana_reminder(user)

                    print(f"Sadhana reminder sent → {user.email}")

    # 12 PM SUMMARY
    elif hour == 12 and minute == 0:

        leaders = CustomUser.objects.filter(
            profile__role='leader'
        )

        for leader in leaders:

            residency = getattr(
                leader.profile,
                'residency',
                'Main Residency'
            )

            already_sent = Notification.objects.filter(
                user=leader,
                type='sadhana_summary_alert',
                created_at__date=now.date()
            ).exists()

            if already_sent:
                continue

            devotees = CustomUser.objects.filter(
                profile__role='devotee',
                profile__residency=residency
            )

            unsubmitted = []

            for devotee in devotees:

                submitted = SadhanaEntry.objects.filter(
                    user=devotee,
                    sadhana_date=now.date()
                ).exists()

                if not submitted:
                    unsubmitted.append(devotee.name)

            if unsubmitted:

                from .services import send_sadhana_summary_alert

                send_sadhana_summary_alert(
                    leader,
                    unsubmitted
                )

                Notification.objects.create(
                    user=leader,
                    message=f"Missing sadhana: {', '.join(unsubmitted)}",
                    type='sadhana_summary_alert'
                )

                print("EMAIL SENT → Sadhana summary")


def scan_inactive_devotees():

    now = timezone.localtime()

    devotees = CustomUser.objects.filter(
        profile__role='devotee'
    )

    for user in devotees:

        recent_alert = Notification.objects.filter(
            user=user,
            type='inactive_alert',
            created_at__gte=now - timedelta(days=7)
        ).exists()

        if recent_alert:
            continue

        recent_sadhana = SadhanaEntry.objects.filter(
            user=user,
            sadhana_date__gte=(now - timedelta(days=7)).date()
        ).exists()

        if not recent_sadhana:

            residency = getattr(
                user.profile,
                'residency',
                'Main Residency'
            )

            leader_emails = get_leader_emails(residency)

            Notification.objects.create(
                user=user,
                message="Inactive devotee alert",
                type='inactive_alert'
            )

            send_inactive_alert(
                user,
                7,
                leader_emails
            )

            print("EMAIL SENT → Inactive alert")


def send_daily_assignment_emails():

    print("DEBUG → send_daily_assignment_emails running")

    today = timezone.localtime().date()

    sevas_today = DailySeva.objects.filter(
        service_date=today,
        assignment_email_sent=False
    )

    print(f"DEBUG → found {sevas_today.count()} sevas")

    for seva in sevas_today:

        user = seva.devotee

        if user and user.email:

            print(f"DEBUG → sending assignment mail to {user.email}")

            send_seva_assigned_notification(user, seva)

            seva.assignment_email_sent = True
            seva.save()

            print("EMAIL SENT → Daily Seva Assignment")


def start_scheduler():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        scan_seva_duties,
        'interval',
        minutes=1,
        id='scan_seva_job',
        replace_existing=True
    )

    scheduler.add_job(
        scan_sadhana_entries,
        'interval',
        minutes=1,
        id='scan_sadhana_job',
        replace_existing=True
    )

    scheduler.add_job(
        scan_inactive_devotees,
        'cron',
        hour=9,
        id='scan_inactive_job',
        replace_existing=True
    )

    # TEMPORARY TESTING
    scheduler.add_job(
        send_daily_assignment_emails,
        'interval',
        minutes=1,
        id='daily_assignment_job',
        replace_existing=True
    )

    scheduler.start()

    print("BhaktiVerse Scheduler Started")