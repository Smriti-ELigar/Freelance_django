# Generated by Django 5.1.4 on 2024-12-20 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_client',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_freelancer',
            field=models.BooleanField(default=False),
        ),
    ]
