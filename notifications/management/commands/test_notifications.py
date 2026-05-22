import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser
from seva.models import WeeklyServiceAssignment, DailySeva
from seva.views import generate_daily_sevas_and_notify
from notifications.scheduler import scan_seva_duties

class Command(BaseCommand):
    help = "Test BhaktiVerse email notification system automated flow"

    def handle(self, *args, **options):
        self.stdout.write("Starting automated notification test...")

        # 1. Fetch or create a test devotee
        devotee = CustomUser.objects.filter(profile__role='devotee').first()
        if not devotee:
            devotee, created = CustomUser.objects.get_or_create(
                email='devotee_test@bhaktiverse.com',
                defaults={'name': 'Test Devotee', 'role': 'Devotee'}
            )
            # Ensure profile exists
            if not hasattr(devotee, 'profile'):
                from accounts.models import Profile
                Profile.objects.create(user=devotee, role='devotee')

        self.stdout.write(f"Using devotee: {devotee.email}")

        # 2. Schedule a test service 2 minutes in the future
        now = timezone.localtime()
        start_dt = now + datetime.timedelta(minutes=2)
        
        self.stdout.write(f"Scheduling weekly assignment at: {start_dt.strftime('%I:%M %p')}")
        
        assignment = WeeklyServiceAssignment.objects.create(
            service_name="Test Deity Worship Seva",
            devotee=devotee,
            residency=getattr(devotee.profile, 'residency', 'Main Residency'),
            start_date=start_dt.date(),
            end_date=start_dt.date(),
            start_time=start_dt.time(),
            duration_minutes=30,
            active=True
        )

        self.stdout.write("Generating DailySeva record...")
        generate_daily_sevas_and_notify(assignment, leader_name="Test Temple Leader")

        # 3. Retrieve the created DailySeva
        daily_seva = DailySeva.objects.filter(weekly_service=assignment).first()
        if not daily_seva:
            self.stderr.write("Failed to create DailySeva record!")
            return

        self.stdout.write(f"Created DailySeva ID: {daily_seva.id}")
        self.stdout.write(f"Initial: reminder_30_sent={daily_seva.reminder_30_sent}, reminder_start_sent={daily_seva.reminder_start_sent}")

        # 4. Run the scheduler to trigger the 30-minute reminder
        self.stdout.write("Running scheduler scan for the 30-minute reminder (since 2 minutes is within the 30-min window)...")
        scan_seva_duties()

        # Reload daily_seva
        daily_seva.refresh_from_db()
        self.stdout.write(f"After Scan 1: reminder_30_sent={daily_seva.reminder_30_sent}, reminder_start_sent={daily_seva.reminder_start_sent}")

        if not daily_seva.reminder_30_sent:
            self.stderr.write("Verification FAILED: 30-minute reminder was NOT triggered!")
            return
        
        self.stdout.write("SUCCESS: 30-minute reminder triggered perfectly.")

        # 5. Simulate that the service time has arrived
        self.stdout.write("Simulating that service time has arrived (updating start time/date to now)...")
        now_local = timezone.localtime()
        daily_seva.service_date = now_local.date()
        daily_seva.service_start_time = (now_local - datetime.timedelta(seconds=5)).time()
        daily_seva.save()

        # 6. Run the scheduler again to trigger the service time reminder
        self.stdout.write("Running scheduler scan for service start time...")
        scan_seva_duties()

        # Reload daily_seva
        daily_seva.refresh_from_db()
        self.stdout.write(f"After Scan 2: reminder_30_sent={daily_seva.reminder_30_sent}, reminder_start_sent={daily_seva.reminder_start_sent}")

        if not daily_seva.reminder_start_sent:
            self.stderr.write("Verification FAILED: Service time reminder was NOT triggered!")
            return

        self.stdout.write("SUCCESS: Service time reminder triggered perfectly.")
        self.stdout.write("ALL TESTS PASSED SUCCESSFULLY! The email notification system is fully operational.")
