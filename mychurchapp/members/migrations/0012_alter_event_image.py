# Generated by Django 4.2.2 on 2023-06-07 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to='members/media'),
        ),
    ]
