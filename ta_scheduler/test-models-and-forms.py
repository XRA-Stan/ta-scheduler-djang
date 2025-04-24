import unittest
from django.test import TestCase
from ta_scheduler.models import User
from datetime import time
from .models import Section, Course
from ta_app.forms import SectionForm, CourseForm, CourseAdminForm,SectionAdminForm
from django.contrib.auth.models import Group




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

    def test_create_course_without_instructor(self):
        course = Course.objects.create(
            courseName='Course Without Instructor',
            sections=self.section
        )
        self.assertIsNone(course.instructor)
        self.assertEqual(course.sections, self.section)

    def test_create_course_without_section(self):
        course = Course.objects.create(
            courseName='Course Without Section',
            instructor=self.instructor
        )
        self.assertIsNone(course.sections)
        self.assertEqual(course.instructor, self.instructor)

    def test_create_course_just_name(self):
        course = Course.objects.create(
            courseName='Minimal Course'
        )
        self.assertIsNone(course.instructor)
        self.assertIsNone(course.sections)

    def test_delete_course(self):
        course = Course.objects.create(
            courseName='Deletable Course',
            sections=self.section,
            instructor=self.instructor
        )
        course_id = course.id
        course.delete()
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course_id)

    def test_delete_section_and_check_course(self):
        # Create a course with a section, then delete the section
        course = Course.objects.create(
            courseName='Course With Section',
            sections=self.section,
            instructor=self.instructor
        )
        self.section.delete()
        course.refresh_from_db()
        self.assertIsNone(course.sections)


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

    def test_delete_section(self):
        section = Section.objects.create(
            sectionName='Lab Delete',
            dayOfWeek='2',
            teaching_assistant=self.ta,
            timeOfDay=time(13, 0)
        )
        section_id = section.id
        section.delete()
        with self.assertRaises(Section.DoesNotExist):
            Section.objects.get(id=section_id)


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



