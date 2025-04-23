import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import time
from .models import Section, Course
from ta_app.forms import SectionForm, CourseForm, CourseAdminForm,SectionAdminForm
from django.contrib.auth.models import Group





class SectionModelTest(TestCase):
    def setUp(self):
        self.ta = User.objects.create_user(username='tauser', password='testpass')

    def test_create_section(self):
        section = Section.objects.create(
            sectionName='Lab A',
            dayOfWeek='1',  # Monday
            teaching_assistant=self.ta,
            timeOfDay=time(14, 30)
        )
        self.assertEqual(section.sectionName, 'Lab A')
        self.assertEqual(section.dayOfWeek, '1')
        self.assertEqual(section.teaching_assistant.username, 'tauser')
        self.assertEqual(section.timeOfDay, time(14, 30))


class CourseModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor', password='testpass', is_staff=True)
        self.section = Section.objects.create(
            sectionName='Lab B',
            dayOfWeek='2',
            timeOfDay=time(10, 0)
        )

    def test_create_course(self):
        course = Course.objects.create(
            courseName='Intro to CS',
            sections=self.section,
            instructor=self.instructor
        )
        self.assertEqual(course.courseName, 'Intro to CS')
        self.assertEqual(course.sections, self.section)
        self.assertEqual(course.instructor, self.instructor)


class SectionFormTest(TestCase):
    def setUp(self):
        self.ta = User.objects.create_user(username='ta', password='test')

    def test_valid_section_form(self):
        form = SectionForm(data={
            'sectionName': 'Lab C',
            'dayOfWeek': '3',
            'teaching_assistant': self.ta.id,
            'timeOfDay': '15:00'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_section_form_missing_time(self):
        form = SectionForm(data={
            'sectionName': 'Lab D',
            'dayOfWeek': '4',
            'teaching_assistant': self.ta.id
            # timeOfDay is missing
        })
        self.assertFalse(form.is_valid())
        self.assertIn('timeOfDay', form.errors)


class CourseFormTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor', password='test', is_staff=True)
        self.section = Section.objects.create(
            sectionName='Lab E',
            dayOfWeek='5',
            timeOfDay=time(11, 45)
        )

    def test_valid_course_form(self):
        form = CourseForm(data={
            'courseName': 'Data Structures',
            'sections': self.section.id,
            'instructor': self.instructor.id
        })
        self.assertTrue(form.is_valid())

#testing that users are filtered by group
class SectionAdminFormTest(TestCase):
    def setUp(self):
        # Create group and assign one user
        self.ta_group = Group.objects.create(name='Teaching Assistants')
        self.ta_user = User.objects.create_user(username='ta_user')
        self.other_user = User.objects.create_user(username='not_ta_user')
        self.ta_group.user_set.add(self.ta_user)

    def test_teaching_assistant_queryset_filtered_by_group(self):
        form = SectionAdminForm()
        self.assertIn(self.ta_user, form.fields['teaching_assistant'].queryset)
        self.assertNotIn(self.other_user, form.fields['teaching_assistant'].queryset)

class CourseAdminFormTest(TestCase):
    def setUp(self):
        # Create group and assign one user
        self.instructor_group = Group.objects.create(name='Instructors')
        self.instructor_user = User.objects.create_user(username='instructor_user')
        self.other_user = User.objects.create_user(username='random_user')
        self.instructor_group.user_set.add(self.instructor_user)

    def test_instructor_queryset_filtered_by_group(self):
        form = CourseAdminForm()
        self.assertIn(self.instructor_user, form.fields['instructor'].queryset)
        self.assertNotIn(self.other_user, form.fields['instructor'].queryset)



