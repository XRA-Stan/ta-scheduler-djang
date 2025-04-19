from django import forms
from ta_scheduler.models import Course
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'instructor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users who are instructors
        self.fields['instructor'].queryset = User.objects.filter(groups__name='Instructor')
