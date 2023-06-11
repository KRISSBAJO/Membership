# Generated by Django 4.2.2 on 2023-06-11 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_finance_expense_customcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='TithlyOffering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('offering', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tithe', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('shiloh', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('thanksgiving', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('welfare', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('project', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_income', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='finance',
            name='tithly_offering',
        ),
    ]