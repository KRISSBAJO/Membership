# Generated by Django 4.2.2 on 2023-06-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_churchattendance_children_churchattendance_men_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchattendance',
            name='other_service_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='churchattendance',
            name='service_type',
            field=models.CharField(choices=[('MID_WK', 'Wednesday Midweek'), ('SUN', 'Sunday'), ('WOSE', 'Week of Spiritual Emphasis'), ('SHILOH', 'Shiloh'), ('ANNI', 'Anniversary'), ('LE_SUB', 'Leadership Empowerment Summit'), ('OTHER', 'Others')], default='SUN', max_length=20),
        ),
    ]
