# Generated by Django 4.2.2 on 2023-06-08 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_alter_event_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='carousel_images/')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='testimonials/')),
                ('text', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='connectcard',
            name='cell_phone',
            field=models.CharField(default=615, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='connectcard',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
