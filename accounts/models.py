from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_answer_1 = models.CharField(max_length=255)
    security_answer_2 = models.CharField(max_length=255)
    security_answer_3 = models.CharField(max_length=255)
