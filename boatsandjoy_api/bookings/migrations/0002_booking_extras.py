# Generated by Django 3.1.5 on 2021-03-09 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='extras',
            field=models.TextField(default=''),
        ),
    ]
