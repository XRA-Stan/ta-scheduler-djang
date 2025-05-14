from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ta_scheduler.models import PublicProfile

User = get_user_model()

class PublicProfileEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='testpass')
        self.profile = PublicProfile.objects.create(
            user=self.user,
            email='alice@example.com',
            bio='',  # Start with empty bio
        )

    #was having issues figuring out the html and views
    def test_edit_public_profile_view_and_html_works(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        profile = PublicProfile.objects.create(user=user, bio="Test bio")
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit_public_profile', kwargs={'username': user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_public_profile_edits_work(self):
        # Log in as the user
        self.client.login(username='alice', password='testpass')

        # Edit bio through POST request
        url = reverse('edit_public_profile', kwargs={'username': 'alice'})
        response = self.client.post(url, {
            'bio': 'Updated bio content',
            'email': 'alice@example.com',  # required in
            'office_location': '',
            'office_hours': '',
        })

        # Check redirect after POST (successful update)
        self.assertEqual(response.status_code, 302)

        # Reload profile from DB and verify update
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio content')