from django import forms
from ta_scheduler.models import Section, Course, DAYS_OF_WEEK
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class SectionForm(forms.ModelForm):
    """Form for creating and editing Section instances"""

    class Meta:
        model = Section
        fields = ['sectionName', 'dayOfWeek', 'teaching_assistant', 'timeOfDay']
        widgets = {
            'sectionName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter section name'}),
            'dayOfWeek': forms.Select(choices=DAYS_OF_WEEK, attrs={'class': 'form-control'}),
            'teaching_assistant': forms.Select(attrs={'class': 'form-control'}),
            'timeOfDay': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        labels = {
            'sectionName': 'Section Name',
            'dayOfWeek': 'Day of Week',
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
        fields = ['sectionName', 'dayOfWeek', 'teaching_assistant', 'timeOfDay']
        widgets = {
            'dayOfWeek': forms.RadioSelect(choices=DAYS_OF_WEEK),
            'timeOfDay': forms.TimeInput(attrs={'type': 'time'}),
        }
        help_texts = {
            'timeOfDay': 'Please enter time in 24-hour format (e.g., 14:30 for 2:30 PM)',
        }

    #filretering by groups, will need to check labels in user groups
    def __init__(self, *args, **kwargs):
        super(SectionAdminForm, self).__init__(*args, **kwargs)
        try:
            ta_group = Group.objects.get(name='Teaching Assistants')
            self.fields['teaching_assistant'].queryset = ta_group.user_set.all()
        except Group.DoesNotExist:
            self.fields['teaching_assistant'].queryset = User.objects.none()


class CourseAdminForm(forms.ModelForm):
    """Enhanced form for Course admin interface"""

    class Meta:
        model = Course
        fields = ['courseName', 'sections', 'instructor']

    # filtering by user group
    def __init__(self, *args, **kwargs):
        super(CourseAdminForm, self).__init__(*args, **kwargs)
        try:
            instructor_group = Group.objects.get(name='Instructors')
            self.fields['instructor'].queryset = instructor_group.user_set.all()
        except Group.DoesNotExist:
            self.fields['instructor'].queryset = User.objects.none()


User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model  = User
        fields = ['full_name', 'email', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        pw = self.cleaned_data.get('password')
        if pw:
            user.set_password(pw)
        if commit:
            user.save()
        return user