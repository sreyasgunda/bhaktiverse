from django.db import models
from django.conf import settings

class SadhanaEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sadhana_entries')
    sadhana_date = models.DateField()
    folk_residency = models.CharField(max_length=50)
    
    # Mangal Aarti options: '4', '3', '2', '1', '0', 'OS', 'Sick', 'AS'
    mangal_aarti = models.CharField(max_length=10)
    
    # Group Japa options: '4', '3', '2', '1', '0', 'OS', 'Sick', 'AS'
    group_japa = models.CharField(max_length=10)
    
    # SB Class options: '2', '1', '0', 'OS', 'Sick', 'AS'
    sb_class = models.CharField(max_length=10)
    
    # Rounds Chanted (1-16)
    rounds_chanted = models.IntegerField()
    
    # Book Reading options: '4', '3', '2', '1', '0'
    sp_reading = models.CharField(max_length=10)
    
    # Assigned Service options: '1', '0', 'OS', 'Sick', 'AS'
    assigned_service = models.CharField(max_length=10)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.sadhana_date}"

class SadhanaLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sadhana_logs')
    date = models.DateField()
    mangala_aarti = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.date} - mangala_aarti={self.mangala_aarti}"
