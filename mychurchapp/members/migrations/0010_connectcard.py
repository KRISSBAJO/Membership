# Generated by Django 4.2.2 on 2023-06-07 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_churchmember_is_inactive_alter_churchmember_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('title', models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Dr', 'Dr'), ('Rev', 'Rev')], max_length=10)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('cell_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married')], max_length=10)),
                ('spouse_name', models.CharField(blank=True, max_length=200, null=True)),
                ('spouse_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('spouse_dob', models.DateField(blank=True, null=True)),
                ('children_names', models.TextField(blank=True, null=True)),
                ('visit_status', models.CharField(choices=[('1st Time Guest', '1st Time Guest'), ('2nd Time Guest', '2nd Time Guest'), ('3rd Time Guest', '3rd Time Guest'), ('Regular Visitor', 'Regular Visitor'), ('Out of Town Guest', 'Out of Town Guest'), ('Member', 'Member')], max_length=20)),
                ('guest_of', models.CharField(blank=True, max_length=200, null=True)),
                ('source', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
