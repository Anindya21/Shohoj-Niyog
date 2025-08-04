from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    
    ROLE_CHOICES= (
        ('interviewer', 'Interviewer'),
        ('candidate', 'Candidate'),
    )

    phone= models.CharField(max_length=11, blank=True, null=True)
    role= models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    def __str__(self):
        return f"{self.username}({self.role})"
    