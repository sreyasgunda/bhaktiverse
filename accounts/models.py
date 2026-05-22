from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    interesting_skills = models.TextField(blank=True, null=True)
    
    ROLE_CHOICES = [
        ('Devotee', 'Devotee'),
        ('Temple Leader', 'Temple Leader'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Devotee')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=[
            ('devotee', 'Devotee'),
            ('leader', 'Temple Leader')
        ],
        default='devotee'
    )
    is_out_of_station = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)
    residency = models.CharField(max_length=100, default='Main Residency')

    def __str__(self):
        return f"{self.user.name} ({self.role})"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role_map = {
            'Devotee': 'devotee',
            'Temple Leader': 'leader',
            'devotee': 'devotee',
            'leader': 'leader',
        }
        db_role = role_map.get(instance.role, 'devotee')
        Profile.objects.create(user=instance, role=db_role)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        role_map = {
            'Devotee': 'devotee',
            'Temple Leader': 'leader',
            'devotee': 'devotee',
            'leader': 'leader',
        }
        db_role = role_map.get(instance.role, 'devotee')
        if instance.profile.role != db_role:
            instance.profile.role = db_role
            instance.profile.save()

