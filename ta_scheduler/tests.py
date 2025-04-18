from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse



# Create your tests here.
class successLogin(TestCase):
    def setUp(self):
        #creation of a test user
        self.username = 'testuser'
        self.password = 'test123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def testloginGood(self):
        #self.client.login will return true or false if the user was logged in or not
        success = self.client.login(username=self.username, password=self.password)
        self.assertTrue(success)

    def testloginRedirect(self):
        #uses urls.py to see if it can reverse from its page back to the login
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        #This will check if a redirect occured AKA redirecting to the home page
        self.assertEqual(response.status_code, 302)

        #Grabs the users info from the response
        user = response.context['user']
        #checks if the user is logged in and wasnt just redirected
        self.assertTrue(user.is_authenticated)

    def testloadCorrectly(self):
        #This refers to the homepage
        response = self.client.get("/")
        #This checks if the home page was loaded correctly
        self.assertEqual(response.status_code, 200)


