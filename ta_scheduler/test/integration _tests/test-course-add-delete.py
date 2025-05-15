from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from ta_scheduler.models import Course, Section

User = get_user_model()


class CourseIntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            role='admin'
        )
        self.login_url = reverse('login')
        self.courses_url = reverse('courses')

    def test_section_create_and_delete(self):
        course = Course.objects.create(courseName='CSC 202', semester='Spring', year=2025)
        instructor = User.objects.create_user(username='instructor', password='instructorpass', role='instructor')

        self.client.login(username='admin', password='adminpass')

        course_detail_url = reverse('course_detail', kwargs={'course_id': course.id})

        create_section_response = self.client.post(course_detail_url, {
            'section_name': 'Lab A',
            'day1': 'Monday',
            'day2': 'Wednesday',
            'start_time': '10:00',
            'end_time': '12:00',
            'teacher': instructor.id
        }, follow=True)
        self.assertEqual(create_section_response.status_code, 200)
        self.assertContains(create_section_response, 'Lab A')

        section = Section.objects.get(sectionName='Lab A', course=course)
        delete_section_response = self.client.post(course_detail_url, {
            'delete_section': section.id
        }, follow=True)
        self.assertEqual(delete_section_response.status_code, 200)
        self.assertNotContains(delete_section_response, 'Lab A')

    def test_create_two_courses_and_delete_second(self):
        self.client.post(self.login_url, {
            'username': 'admin',
            'password': 'adminpass'
        })

        self.client.post(self.courses_url, {
            'course_name': 'CSC 101',
            'semester': 'Fall',
            'year': '2025'
        })

        self.client.post(self.courses_url, {
            'course_name': 'CSC 202',
            'semester': 'Spring',
            'year': '2025'
        })

        courses = Course.objects.all()
        self.assertEqual(courses.count(), 2)

        csc202 = Course.objects.get(courseName='CSC 202')
        self.client.post(self.courses_url, {
            'delete_course_id': csc202.id
        }, follow=True)

        courses = Course.objects.all()
        self.assertEqual(courses.count(), 1)
        self.assertEqual(courses.first().courseName, 'CSC 101')
