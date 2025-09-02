from django.db import migrations

def create_demo_doctors(apps, schema_editor):
    User = apps.get_model('core', 'User')
    DoctorProfile = apps.get_model('core', 'DoctorProfile')

    doctor1 = User.objects.create_user(
        username='dr.adams',
        first_name='Emily',
        last_name='Adams',
        email='dradams@ehospital.com',
        password='doctorpass',
        role='DOCTOR'
    )
    DoctorProfile.objects.create(user=doctor1, specialization='Cardiology', license_number='DOC001')

    doctor2 = User.objects.create_user(
        username='dr.baker',
        first_name='John',
        last_name='Baker',
        email='drbaker@ehospital.com',
        password='doctorpass',
        role='DOCTOR'
    )
    DoctorProfile.objects.create(user=doctor2, specialization='Neurology', license_number='DOC002')

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_demo_doctors),
    ]