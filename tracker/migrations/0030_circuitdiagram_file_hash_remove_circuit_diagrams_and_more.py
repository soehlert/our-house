# Generated by Django 5.2.1 on 2025-06-06 15:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0029_device_attached_appliance'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuitdiagram',
            name='file_hash',
            field=models.CharField(blank=True, db_index=True, max_length=32),
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='diagrams',
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(choices=[('Receptacle', 'Receptacle'), ('Switch', 'Switch'), ('Light', 'Light'), ('Detector', 'Detector'), ('Ceiling Fan', 'Ceiling Fan'), ('Floor Heating', 'Floor Heating')], max_length=50),
        ),
        migrations.AddField(
            model_name='circuit',
            name='diagrams',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='circuits', to='tracker.circuitdiagram'),
        ),
    ]
