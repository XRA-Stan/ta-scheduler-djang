import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import time
from .models import Section, Course
from ta_app.forms import SectionForm, CourseForm, CourseAdminForm,SectionAdminForm
from django.contrib.auth.models import Group
from .models import Course, CourseInstructor




 #unit tests for models and forms
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

    def test_create_section_without_ta(self):
        section = Section.objects.create(
            sectionName='No TA Lab',
            dayOfWeek='1',
            timeOfDay=time(9, 0)
        )
        self.assertIsNone(section.teaching_assistant)
        self.assertEqual(section.sectionName, 'No TA Lab')
        self.assertEqual(section.dayOfWeek, '1')


class CourseModelTest(TestCase):
    def setUp(self):
        # Create a user for instructor (though not used directly in Course)
        self.instructor = User.objects.create_user(username='instructor', password='test', is_staff=True)

        # Create a course
        self.course = Course.objects.create(
            courseName='Intro to CS',
        )

    def test_create_course(self):
        # Test creating a course with a valid name
        self.assertEqual(self.course.courseName, 'Intro to CS')

    def test_course_str_method(self):
        # Test the __str__ method of the Course model
        self.assertEqual(str(self.course), 'Intro to CS')

    def test_create_multiple_courses(self):
        # Test creating multiple courses
        course2 = Course.objects.create(courseName='Data Structures')
        course3 = Course.objects.create(courseName='Algorithms')

        self.assertEqual(course2.courseName, 'Data Structures')
        self.assertEqual(course3.courseName, 'Algorithms')


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
        self.course = Course.objects.create(courseName='Data Structures')


    def test_valid_course_form(self):
        form = CourseForm(data={
            'courseName': 'Data Structures',

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

#removed test for course, since it no loger has an instructor field

class CourseInstructorTests(TestCase):
    def setUp(self):
        # Create instructor
        self.bob = User.objects.create_user(username='bob', password='testpass')
        self.alice = User.objects.create_user(username='alice', password='testpass')

        # Create courses
        self.cs101 = Course.objects.create(courseName="CS101")
        self.cs102 = Course.objects.create(courseName="CS102")

        # Assign bob to two courses
        CourseInstructor.objects.create(course=self.cs101, instructor=self.bob)
        CourseInstructor.objects.create(course=self.cs102, instructor=self.bob)

        # Assign alice to one course
        CourseInstructor.objects.create(course=self.cs101, instructor=self.alice)

    def test_instructor_teaches_multiple_courses(self):
        courses = [ci.course for ci in CourseInstructor.objects.filter(instructor=self.bob)]
        self.assertEqual(len(courses), 2)
        self.assertIn(self.cs101, courses)
        self.assertIn(self.cs102, courses)

    def test_course_has_multiple_instructors(self):
        instructors = [ci.instructor for ci in CourseInstructor.objects.filter(course=self.cs101)]
        self.assertEqual(len(instructors), 2)
        self.assertIn(self.bob, instructors)
        self.assertIn(self.alice, instructors)

