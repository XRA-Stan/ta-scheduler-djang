from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [('admin', 'Admin'), ('instructor', 'Instructor'), ('ta', 'TA'),]

    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices = ROLE_CHOICES)

    def __str__(self):
        return self.full_name