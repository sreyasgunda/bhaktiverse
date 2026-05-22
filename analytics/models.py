from django.db import models
from django.conf import settings

class ProgressStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_stats')
    total_submitted_days = models.IntegerField(default=0)
    percentage_completed = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.email} - Progress: {self.percentage_completed}%"
