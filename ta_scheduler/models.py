from django.db import models
from django.contrib.auth.models import User  # Built-in User model

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name}"


