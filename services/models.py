from django.db import models
from django.conf import settings  
from django.utils import timezone


# Create your models here.
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('web_dev', 'Web Development'),
        ('design', 'Design'),
        ('writing', 'Writing'),
        ('marketing', 'Marketing'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
     # Abstract string reference to avoid circular import

    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='services')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)  # New field to track payment status


    def __str__(self):
        return self.title
    
    # category = models.ForeignKey('Category', on_delete=models.CASCADE)

# services/models.py
class Booking(models.Model):
    client = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    payment_status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ], default='pending')
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line

    def __str__(self):
        return f"{self.client} - {self.service}"

