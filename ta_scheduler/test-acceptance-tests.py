from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ta_scheduler.models import Section, Course
from datetime import time


#acceptance test, admin can log in, and create a course
class AdminCourseCreationTest(TestCase):
    def setUp(self):
        # create a superuser/admin account
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )

        # create a test section for course assignment
        # not used right now
        self.test_section = Section.objects.create(
            sectionName='Test Section 101',
            dayOfWeek='1',  # Monday
            timeOfDay=time(14, 30)  # 2:30 PM
        )

        self.client = Client()

    def test_admin_course_creation(self):
        # 1. Login as admin
        login_successful = self.client.login(username='admin', password='adminpassword123')
        self.assertTrue(login_successful, "Admin login failed")

        # 2. Navigate to home page (should redirect if login successful)
        home_response = self.client.get(reverse('home'))
        self.assertEqual(home_response.status_code, 200, "Failed to access home page after login")

        # 3. Access course creation page
        create_course_response = self.client.get(reverse('create_course'))
        self.assertEqual(create_course_response.status_code, 200, "Failed to access course creation page")

        # 4. Submit a new course
        course_data = {
            'course_name': 'Test Course 101',
            'course_section': self.test_section.id,
            'course_instructor': self.admin_user.id
        }

        # Update the URL to the one you're testing
        create_response = self.client.post(reverse('courses'), data=course_data)
        self.assertEqual(create_response.status_code, 302, "Course creation form submission failed")

        # 5. Verify course was created
        new_course = Course.objects.filter(courseName='Test Course 101').first()
        self.assertIsNotNone(new_course, "Course was not created in database")
        self.assertEqual(new_course.sections, self.test_section, "Section was not properly assigned")
        self.assertEqual(new_course.instructor, self.admin_user, "Instructor was not properly assigned")

        # New test: Create course with no section or instructor
        # same as above just missing some fields
        # and asserting assertIsNone for section and instructor
    def test_admin_course_creation_no_section_instructor(self):
        # 1. Login as admin
        login_successful = self.client.login(username='admin', password='adminpassword123')
        self.assertTrue(login_successful, "Admin login failed")

        # 2. Navigate to home page (should redirect if login successful)
        home_response = self.client.get(reverse('home'))
        self.assertEqual(home_response.status_code, 200, "Failed to access home page after login")

        # 3. Access course creation page
        create_course_response = self.client.get(reverse('create_course'))
        self.assertEqual(create_course_response.status_code, 200, "Failed to access course creation page")

        # 4. Submit a new course with no section or instructor
        course_data_no_section_instructor = {
            'course_name': 'Test Course 102',  # New course name
            'course_section': '',  # No section
            'course_instructor': '',  # No instructors
        }

        create_response_no_section_instructor = self.client.post(reverse('courses'),
                                                                 data=course_data_no_section_instructor)
        self.assertEqual(create_response_no_section_instructor.status_code, 302,
                         "Course creation form submission failed without section or instructor")

        # 5. Verify course was created (no section and no instructor)
        new_course_no_section_instructor = Course.objects.filter(courseName='Test Course 102').first()
        self.assertIsNotNone(new_course_no_section_instructor, "Course was not created in database")
        self.assertIsNone(new_course_no_section_instructor.sections, "Course should not have a section")
        self.assertIsNone(new_course_no_section_instructor.instructor, "Course should not have an instructor")