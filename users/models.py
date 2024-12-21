import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Freelancer', 'Freelancer'),
        ('Client', 'Client'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Client')
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    # email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_token = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    is_verified = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # Ensure only one of is_freelancer or is_client is True
        if self.is_freelancer:
            self.is_client = False
        elif self.is_client:
            self.is_freelancer = False
        else:
            # Set role-based boolean fields
            if self.role == 'Freelancer':
                self.is_freelancer = True
                self.is_client = False
            elif self.role == 'Client':
                self.is_client = True
                self.is_freelancer = False

        super(CustomUser, self).save(*args, **kwargs)



    # service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    # client = models.ForeignKey('auth.User', on_delete=models.CASCADE)

