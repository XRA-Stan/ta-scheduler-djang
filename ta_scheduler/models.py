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

# Create your models here.

class Section(models.Model):
    sectionName = models.CharField(max_length=100)
    dayOfWeek = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    teaching_assistant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="ta_sections", null=True, blank=True)
    teaching_assistant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="ta_sections",
        null=True, blank=True,
        limit_choices_to={'role': 'ta'}
    )

    timeOfDay = models.TimeField(
        default=time(0, 0),
        help_text="This field expects time in 24-hour format (HH:MM)."
        # this is not showing up in the add section of admin page in django
        # the timeOfDay field is in 24 hour time, i would like to have a little comment under the field
        # so that the user can see that

        # the docs page https://docs.djangoproject.com/en/5.2/ref/models/fields/ says that this becomes
        # (this is probably not necessary since the actual profiles html will interface the admin page to do stuff)
    )
    def __str__(self):
        return self.sectionName

class Course(models.Model):
    courseName = models.CharField(max_length=100)
    sections = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="courses",null=True,blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="courses_teaching",null=True,blank=True)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="courses_teaching",
        null=True, blank=True,
        limit_choices_to={'role': 'instructor'}
    )

    def __str__(self):
        return self.courseName

