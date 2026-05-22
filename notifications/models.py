from django.db import models
from django.conf import settings
from seva.models import DailySeva

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    seva_duty = models.ForeignKey(DailySeva, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.message[:30]}..."
