# Generated by Django 4.2.2 on 2023-06-06 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_cellgroup_city_cellgroup_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cellgroup',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='servicegroup',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
