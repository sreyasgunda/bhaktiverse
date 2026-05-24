from django.db import migrations

def create_temples(apps, schema_editor):
    Temple = apps.get_model('temple', 'Temple')
    Profile = apps.get_model('accounts', 'Profile')
    # Gather unique residency values, strip and capitalize for consistency
    residencies = set()
    for profile in Profile.objects.all():
        if profile.residency:
            residencies.add(profile.residency.strip())
    for name in residencies:
        Temple.objects.get_or_create(name=name)

def assign_temple_to_profiles(apps, schema_editor):
    Temple = apps.get_model('temple', 'Temple')
    Profile = apps.get_model('accounts', 'Profile')
    for profile in Profile.objects.all():
        if profile.residency:
            temple_name = profile.residency.strip()
            try:
                temple = Temple.objects.get(name=temple_name)
                profile.temple = temple
                profile.save(update_fields=['temple'])
            except Temple.DoesNotExist:
                # If for some reason temple not created, skip
                continue

class Migration(migrations.Migration):
    dependencies = [
        ('temple', '0001_initial'),
        ('accounts', '0005_profile_temple'),
    ]

    operations = [
        migrations.RunPython(create_temples, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(assign_temple_to_profiles, reverse_code=migrations.RunPython.noop),
    ]
