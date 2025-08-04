from django.db import models
from django.utils import timezone

# Create your models here.

class QAPair(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    print("QAPair model loaded")

    # def __str__(self):
    #     return f"Q: {self.question} | A: {self.answer}"

