from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import time



# django didn't give me an option to select days of the week for the week without it looking terrible
# so a tuple is created and the integer field is replaced with a field for days of the week


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'), ('instructor', 'Instructor'), ('ta', 'TA'),
    ]
    full_name = models.CharField(max_length=100)
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.full_name



DAYS_OF_WEEK = [
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
    ('7', 'Sunday'),
]

class Course(models.Model):
    courseName = models.CharField(max_length=100)

    def __str__(self):
        return self.courseName


class Section(models.Model):
    sectionName = models.CharField(max_length=100)
    dayOfWeek = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections", null=True, blank=True)
    teaching_assistant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="ta_sections", null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="sections_taught", null=True, blank=True)
    timeOfDay = models.TimeField(
        default=time(0, 0),
        help_text="This field expects time in 24-hour format (HH:MM)."
    )

    def __str__(self):
        return self.sectionName


class CourseInstructor(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.instructor.username} teaches {self.course.courseName}"


