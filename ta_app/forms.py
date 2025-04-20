from django import forms
from ta_scheduler.models import Section, Course, daysOfWeek
from django.contrib.auth.models import User


class SectionForm(forms.ModelForm):
    """Form for creating and editing Section instances"""

    class Meta:
        model = Section
        fields = ['sectionName', 'daysOfWeek', 'teaching_assistant', 'timeOfDay']
        widgets = {
            'sectionName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter section name'}),
            'daysOfWeek': forms.Select(choices=daysOfWeek, attrs={'class': 'form-control'}),
            'teaching_assistant': forms.Select(attrs={'class': 'form-control'}),
            'timeOfDay': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        labels = {
            'sectionName': 'Section Name',
            'daysOfWeek': 'Day of Week',
            'teaching_assistant': 'Teaching Assistant',
            'timeOfDay': 'Time of Day',
        }
        help_texts = {
            'timeOfDay': 'Please enter time in 24-hour format (e.g., 14:30 for 2:30 PM)',
        }


class CourseForm(forms.ModelForm):
    """Form for creating and editing Course instances"""

    class Meta:
        model = Course
        fields = ['courseName', 'sections', 'instructor']
        widgets = {
            'courseName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
            'sections': forms.Select(attrs={'class': 'form-control'}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'courseName': 'Course Name',
            'sections': 'Section',
            'instructor': 'Instructor',
        }


# Additional admin-friendly forms

class SectionAdminForm(forms.ModelForm):
    """Enhanced form for Section admin interface"""

    class Meta:
        model = Section
        fields = ['sectionName', 'daysOfWeek', 'teaching_assistant', 'timeOfDay']
        widgets = {
            'daysOfWeek': forms.RadioSelect(choices=daysOfWeek),
            'timeOfDay': forms.TimeInput(attrs={'type': 'time'}),
        }
        help_texts = {
            'timeOfDay': 'Please enter time in 24-hour format (e.g., 14:30 for 2:30 PM)',
        }


class CourseAdminForm(forms.ModelForm):
    """Enhanced form for Course admin interface"""

    class Meta:
        model = Course
        fields = ['courseName', 'sections', 'instructor']

    # If you want to filter TAs and instructors to only show staff users
    def __init__(self, *args, **kwargs):
        super(CourseAdminForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = User.objects.filter(is_staff=True)