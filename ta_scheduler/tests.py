from django.test import TestCase
from django.contrib.auth.models import User, Group
from ta_app.forms import CourseForm




class CourseFormTest(TestCase):

    def setUp(self):
        self.instructor_group = Group.objects.create(name='Instructor')
        self.instructor_user = User.objects.create_user(username='instructor', password='testpassword')
        self.instructor_user.groups.add(self.instructor_group)

    def test_course_form_valid(self):
        # Test when it's filled out correctly
        form_data = {
            'name': 'Test Course',
            'code': 'CS101',
            'description': 'A test course.',
            'instructor': self.instructor_user.id,
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())  # The form should be valid

    def test_course_form_invalid_instructor(self):
        # Test when an invalid instructor is selected
        invalid_instructor = User.objects.create_user(username='student', password='testpassword')
        form_data = {
            'name': 'Test Course',
            'code': 'CS101',
            'description': 'A test course.',
            'instructor': invalid_instructor.id,  # Student shouldn't be an instructor
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())  # The form should be invalid because this user is not an instructor
