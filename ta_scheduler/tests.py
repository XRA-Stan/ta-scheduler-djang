from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse



# Create your tests here.
class SuccessLogin(TestCase):
    def setUp(self):
        #creation of a test user
        self.username = 'testuser'
        self.password = 'test123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def testLoginGood(self):
        #self.client.login will return true or false if the user was logged in or not
        success = self.client.login(username=self.username, password=self.password)
        self.assertTrue(success)

    def testLoginRedirect(self):
        #uses urls.py to see if it can reverse from its page back to the login
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        #This will check if a redirect occured AKA redirecting to the home page
        self.assertEqual(response.status_code, 302)

        #Grabs the users info from the response
        user = response.context['user']
        #checks if the user is logged in and wasnt just redirected
        self.assertTrue(user.is_authenticated)

    def testLoadCorrectly(self):
        #This refers to the homepage
        response = self.client.get("/")
        #This checks if the home page was loaded correctly
        self.assertEqual(response.status_code, 200)

class FailedLogin(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'test123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def testWrongUsername(self):
        login = self.client.login(username= 'wrongUsername', password=self.password)
        self.assertFalse(login)

    def testWrongPassword(self):
        login = self.client.login(username= self.username, password= "wrongPassword")
        self.assertFalse(login)

    def testNoRedirect(self):
        response = self.client.post(reverse('login'), {'username': "wrong", 'password': self.password})
        self.assertNotEqual(response.status_code, 302)

        user = response.context['user']
        self.assertFalse(user.is_authenticated)

    def testCapsUsername(self):
        login = self.client.login(username= 'TESTUSER', password= self.password)
        self.assertFalse(login)

    def testCapsPassword(self):
        login = self.client.login(username= self.username, password= "TEST123")
        self.assertFalse(login)




