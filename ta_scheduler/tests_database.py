import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import time
from .models import Section, Course
from ta_app.forms import SectionForm, CourseForm


class SectionModelTest(TestCase):
    def setUp(self):
        self.ta = User.objects.create_user(username='tauser', password='testpass')

    def test_create_section(self):
        section = Section.objects.create(
            sectionName='Lab A',
            Day_Of_Week='1',  # Monday
            teaching_assistant=self.ta,
            timeOfDay=time(14, 30)
        )
        self.assertEqual(section.sectionName, 'Lab A')
        self.assertEqual(section.Day_Of_Week, '1')
        self.assertEqual(section.teaching_assistant.username, 'tauser')
        self.assertEqual(section.timeOfDay, time(14, 30))


class CourseModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor', password='testpass', is_staff=True)
        self.section = Section.objects.create(
            sectionName='Lab B',
            Day_Of_Week='2',
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
            'Day_Of_Week': '3',
            'teaching_assistant': self.ta.id,
            'timeOfDay': '15:00'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_section_form_missing_time(self):
        form = SectionForm(data={
            'sectionName': 'Lab D',
            'Day_Of_Week': '4',
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
            Day_Of_Week='5',
            timeOfDay=time(11, 45)
        )

    def test_valid_course_form(self):
        form = CourseForm(data={
            'courseName': 'Data Structures',
            'sections': self.section.id,
            'instructor': self.instructor.id
        })
        self.assertTrue(form.is_valid())

