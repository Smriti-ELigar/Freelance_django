# Generated by Django 5.1.4 on 2024-12-21 01:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_is_client_customuser_is_freelancer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email_verification_token',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
