from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUser(AbstractUser):
    
    ROLE_CHOICES= (
        ('interviewer', 'Interviewer'),
        ('candidate', 'Candidate'),
    )

    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    email= models.EmailField(unique=True)

    phone= models.CharField(max_length=11, blank=True, null=True)
    role= models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    company = models.CharField(max_length=30, blank=True, null=True)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username','role','phone']
    
    def __str__(self):
        return f"{self.email}({self.role})"
    
    def clean(self):
        super().clean()
        if self.role == 'interviewer' and not self.company:
            raise ValidationError({'company': 'Company is required for interviewers.'})
    