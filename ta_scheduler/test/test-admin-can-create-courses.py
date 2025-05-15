from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ta_scheduler.models import Course, Section
from django.utils import timezone

User = get_user_model()


class CourseSectionAcceptanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass',
            role='admin',
            email='admin@example.com'
        )
        self.client.login(username='adminuser', password='adminpass')

    def test_course_creation(self):
        response = self.client.post(reverse('courses'), {
            'course_name': 'CS101',
            'semester': 'Fall',
            'year': '2025'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(courseName='CS101', semester='Fall', year=2025).exists())

    def test_section_creation(self):
        course = Course.objects.create(courseName='CS102', semester='Spring', year='2025')
        ta_user = User.objects.create_user(username='tauser', password='tapass', role='ta')

        response = self.client.post(reverse('course_detail', args=[course.id]), {
            'section_name': 'Lab A',
            'day1': 'Monday',
            'day2': 'Wednesday',
            'start_time': '10:00',
            'end_time': '11:30',
            'teacher': ta_user.id
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Section.objects.filter(sectionName='Lab A', course=course).exists())

    def test_invalid_user_cannot_create_course(self):
        self.client.logout()
        normal_user = User.objects.create_user(username='student', password='pass', role='ta')
        self.client.login(username='student', password='pass')

        response = self.client.post(reverse('courses'), {
            'course_name': 'CS999',
            'semester': 'Fall',
            'year': '2025'
        })

        # Should deny and not make anything
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Course.objects.filter(courseName='CS999').exists())
