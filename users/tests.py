from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user, get_user_model, authenticate, login
from django.urls import reverse
import settings
import re

class UserDetails():
    def __init__(self):
        self.id = 0

    def get_user_details(self):
        self.id = self.id + 1
        return {"username": "testee" + str(self.id), 
                "email": "testee" + str(self.id) + "@bob.com",
                "password": "bob"}


class UserModelTests(TestCase):
    def setUp(self):
        self.userDetail = UserDetails()

    def test_user_profile_is_created_when_user_is_created(self):
        """
            tests that a profile is created when a user is created
        """
        userDetails = self.userDetail.get_user_details()
        user = get_user_model().objects.create_user(username=userDetails['username'], 
                                                    password=userDetails['password'],
                                                    email=userDetails['email'])
        self.assertIsNotNone(user.profile)

    def test_user_profile_has_personal_statement_field(self):
        """
            tests that the personal_statement field is created in the profile object
        """
        userDetails = self.userDetail.get_user_details()
        user = get_user_model().objects.create_user(username=userDetails['username'], 
                                                    password=userDetails['password'],
                                                    email=userDetails['email'])
        self.assertIsNotNone(user.profile.personal_statement)

    def test_user_is_not_active_when_user_is_created(self):
        """
            tests that user.is_active is set to false
        """
        userDetails = self.userDetail.get_user_details()
        user = get_user_model().objects.create_user(username=userDetails['username'], 
                                                    password=userDetails['password'],
                                                    email=userDetails['email'])
        self.assertFalse(user.is_active)

    def test_user_is_active_when_user_is_saved(self):
        """
            tests the model signal 'set_is_active_to_false' user.is_active is not
            set to false when user is saved
        """
        userDetails = self.userDetail.get_user_details()  
        user = get_user_model().objects.create_user(username=userDetails['username'], 
                                                    password=userDetails['password'],
                                                    email=userDetails['email'])
        user.is_active = True
        user.save()
        self.assertTrue(user.is_active)



class LoginTests(TestCase):
    def setUp(self):
        self.userDetail = UserDetails()
        self.factory = RequestFactory()

    def test_user_login_redirect(self):
        userDetails = self.userDetail.get_user_details()  
        user = get_user_model().objects.create_user(username=userDetails['username'], 
                                             email=userDetails['email'])
        user.is_active = True
        user.save()
        request = self.factory.get(reverse('users:login'))
        authenticate(request, username=user.username, password=user.password)
        logged_in = self.client.force_login(user)
        response = self.client.get(reverse('users:login'))
        self.assertRedirects(response=response, 
                             expected_url=reverse('users:dashboard'), 
                             status_code=302, 
                             target_status_code=200, 
                             msg_prefix='', 
                             fetch_redirect_response=True)


class DashboardTests(TestCase):
    def setUp(self):
        self.userDetail = UserDetails()
        self.factory = RequestFactory()

    def test_user_logged_out_redirect(self):
        """
            A user that isn't logged in should be redirected from dashboard to login
        """ 
        response = self.client.get(reverse('users:dashboard'))
        self.assertRedirects(response=response, 
                             expected_url='/users/accounts/login/?next=/users/dashboard/', 
                             status_code=302, 
                             target_status_code=200, 
                             msg_prefix='', 
                             fetch_redirect_response=True)

    def test_user_no_access_to_dashboard_if_not_active(self):
        """
            user should be redirected to login if they try and access
            the dashboard but haven't confirmed their email.
        """
        userDetails = self.userDetail.get_user_details()
        user = get_user_model().objects.create_user(username=userDetails['username'],
                                                    password=userDetails['password'],
                                                    email=userDetails['email'])
        self.assertFalse(user.is_active)
        response = self.client.get(reverse('users:dashboard'))
        self.assertRedirects(response=response, 
                     expected_url='/users/accounts/login/?next=/users/dashboard/', 
                     status_code=302, 
                     target_status_code=200, 
                     msg_prefix='', 
                     fetch_redirect_response=True)


class RegisterTests(TestCase):
    def setUp(self):
        self.userDetail = UserDetails()

    def test_user_registers_success(self):
        userDetails = self.userDetail.get_user_details()
        settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        self.client.post(reverse('users:register'), {
            "email": userDetails['email'], 
            "password1": userDetails['password'], 
            "password2": userDetails['password'], 
            "username": userDetails['username']})
        self.assertEqual(get_user_model().objects.filter(username=userDetails['username']).count(), 1)


