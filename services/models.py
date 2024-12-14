from django.db import models
from django.conf import settings  

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title