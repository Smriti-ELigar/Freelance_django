from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Freelancer', 'Freelancer'),
        ('Client', 'Client'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Client')
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)




# this code extends the standard Django user model to include a new field role with specific choices,
# making it easy to differentiate between Freelancer and Client roles within your application.

# AbstractUser is imported from django.contrib.auth.models. It provides all the fields and methods necessary for user authentication.

# models is imported from django.db. This module contains classes and functions used to define the data models in Django.

# Inheritance: The CustomUser class inherits from AbstractUser, meaning it includes all the standard user fields like username, password, email, etc.

# ROLE_CHOICES: This is a class attribute that defines a list of tuples. Each tuple consists of two elements:

# The first element ('Freelancer' or 'Client') is the actual value that will be stored in the database.

# The second element ('Freelancer' or 'Client') is the human-readable name for the choice.

# role: This is a field added to the CustomUser class to store the user's role. It uses Django's CharField with the following parameters:

# max_length=20: Sets the maximum length of the field to 20 characters.

# choices=ROLE_CHOICES: Limits the values of the field to the options provided in ROLE_CHOICES.

# default='Client': Sets the default value of the field to 'Client'.