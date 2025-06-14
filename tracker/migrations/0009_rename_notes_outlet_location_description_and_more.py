# Generated by Django 5.2.1 on 2025-05-29 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_outlet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outlet',
            old_name='notes',
            new_name='location_description',
        ),
        migrations.AlterField(
            model_name='outlet',
            name='device_type',
            field=models.CharField(choices=[('RECEPTACLE', 'Receptacle'), ('SWITCH', 'Switch'), ('LIGHT', 'Light')], max_length=50),
        ),
    ]
