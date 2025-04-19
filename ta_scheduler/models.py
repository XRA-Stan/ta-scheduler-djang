from django.db import models
from django import forms

# django didn't give me an option to select days of the week for the week without it looking terrible
# so a tuple is created and the integer field is replaced with a field for days of the week

daysOfWeek = [
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
    dayOfWeek = models.Field(choices=daysOfWeek, default = '1')

    timeOfDay = models.TimeField(
        db_comment="In 24 hour time"
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
    sections = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.courseName