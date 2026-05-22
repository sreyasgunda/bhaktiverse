from django.db import models
from django.conf import settings
from django.utils import timezone

class MasterService(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class WeeklyServiceAssignment(models.Model):
    service_name = models.CharField(max_length=255)
    devotee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weekly_assignments')
    residency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_name} for {self.devotee.email} ({self.start_date} to {self.end_date})"

class DailySeva(models.Model):
    weekly_service = models.ForeignKey(WeeklyServiceAssignment, on_delete=models.CASCADE, related_name='daily_sevas')
    devotee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_sevas')
    service_name = models.CharField(max_length=255)
    seva_date = models.DateField()
    start_datetime = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    completed = models.BooleanField(default=False)
    reminder_10_sent = models.BooleanField(default=False)
    reminder_start_sent = models.BooleanField(default=False)
    last_reminder_sent = models.DateTimeField(null=True, blank=True)

    # --- NEW REQUIRED DATABASE FIELDS ---
    service_date = models.DateField(null=True, blank=True)
    service_start_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending') # pending / completed
    reminder_30_sent = models.BooleanField(default=False)
    last_reminder_time = models.DateTimeField(null=True, blank=True)

    # --- NEW SCHEDULER SAFETY FIELDS ---
    overdue_alert_sent = models.BooleanField(default=False)
    assignment_email_sent = models.BooleanField(default=False)

    # --- BACKWARD COMPATIBILITY PROPERTIES ---
    @property
    def title(self):
        return self.service_name

    @property
    def start_time(self):
        return self.start_datetime

    @property
    def end_time(self):
        return self.start_datetime + timezone.timedelta(minutes=self.duration_minutes)

    @property
    def is_completed(self):
        return self.completed

    @is_completed.setter
    def is_completed(self, value):
        self.completed = value

    @property
    def user(self):
        return self.devotee

    # --- SYNCHRONIZATION AND SAFETY RULES ON SAVE ---
    def save(self, *args, **kwargs):
        # 1. Date synchronization
        if self.seva_date and not self.service_date:
            self.service_date = self.seva_date
        elif self.service_date and not self.seva_date:
            self.seva_date = self.service_date
        elif self.seva_date and self.service_date:
            # Safety Rule: seva_date should always match service_date
            self.seva_date = self.service_date

        # 2. Time/Datetime synchronization
        if self.start_datetime and not self.service_start_time:
            local_dt = timezone.localtime(self.start_datetime)
            self.service_start_time = local_dt.time()
        elif self.service_date and self.service_start_time:
            # Safety Rule: start_datetime should always be generated from service_date + service_start_time
            naive_dt = timezone.datetime.combine(self.service_date, self.service_start_time)
            generated_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
            if self.start_datetime != generated_dt:
                self.start_datetime = generated_dt

        # 3. Status synchronization
        if self.completed and self.status != 'completed':
            self.status = 'completed'
        elif self.status == 'completed' and not self.completed:
            self.completed = True
        elif not self.completed and self.status == 'completed':
            self.status = 'pending'
        elif self.status == 'pending' and self.completed:
            self.completed = False

        # 4. Last Reminder synchronization
        if self.last_reminder_sent and not self.last_reminder_time:
            self.last_reminder_time = self.last_reminder_sent
        elif self.last_reminder_time and not self.last_reminder_sent:
            self.last_reminder_sent = self.last_reminder_time

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_name} - {self.devotee.email} on {self.seva_date}"


