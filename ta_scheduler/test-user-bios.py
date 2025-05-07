from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import PrivateProfile

User = get_user_model()

class PrivateProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_valid_phone_number_saves(self):
        profile = PrivateProfile(
            user=self.user,
            phone_number='1234567890'
        )
        try:
            profile.save()
        except ValueError:
            self.fail("Valid phone number raised ValueError unexpectedly!")

    def test_invalid_phone_number_raises_error(self):
        profile = PrivateProfile(
            user=self.user,
            phone_number='123-456-7890'  # contains non-digit characters
        )
        with self.assertRaises(ValueError):
            profile.save()

    def test_blank_phone_number_saves(self):
        profile = PrivateProfile(
            user=self.user,
            phone_number=''  # allowed because blank=True
        )
        try:
            profile.save()
        except ValueError:
            self.fail("Blank phone number raised ValueError unexpectedly!")
