
from django.shortcuts import reverse
from django.test import TestCase

from sustainability.models import Userprofile

class TestLogin(TestCase):
    def setUp(self):
        self.user = Userprofile.objects.create_user(username='test_user', email='test_email', password='test_password')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 302, msg="Login did not redirect properly")
        self.assertRedirects(response, reverse('home'), msg_prefix="Login did not redirect to home page")
        self.assertIn('_auth_user_id', self.client.session, msg="User not authenticated after login")

    def test_wrong_username(self):
        response = self.client.post(reverse('login'), {'username': 'test_user_wrong', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200, msg="Login with wrong username did not return status code 200")
        self.assertNotIn('_auth_user_id', self.client.session, msg="User authenticated despite wrong username")
        # Assert error message
        test_messages = list(response.context['messages'])
        self.assertEqual(len(test_messages), 1, msg="Error message not set")
        self.assertEqual(test_messages[0].message, "Invalid username or password", msg="Incorrect error message")

    def test_wrong_password(self):
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': 'test_password_wrong'})
        self.assertEqual(response.status_code, 200, msg="Login with wrong password did not return status code 200")
        self.assertNotIn('_auth_user_id', self.client.session, msg="User authenticated despite wrong password")
        test_messages = list(response.context['messages'])
        self.assertEqual(len(test_messages), 1, msg="Error message not set")
        self.assertEqual(test_messages[0].message, "Invalid username or password", msg="Incorrect error message")

    def test_logout(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302, msg="Logout did not redirect properly")
        self.assertNotIn('_auth_user_id', self.client.session, msg="User still authenticated after logout")
