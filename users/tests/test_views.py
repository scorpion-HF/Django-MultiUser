from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import NormalProfile, SupervisorProfile


class NormalUserSignUpViewTest(TestCase):

    def setUp(self):
        self.url = reverse('normal-signup')
        User = get_user_model()
        user = User.objects.create_user(email='supervisor@mail.com', password='test123456', is_supervisor=True)
        self.client.login(username=user.email, password='test123456')

    def test_get_request_no_supervisor(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_request_supervisor(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_request_valid_form(self):
        data = {
            'email': 'normal@user.com',
            'password1': 'FooBar123456',
            'password2': 'FooBar123456',
            'normal_user_id': '12345',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('normal-signup'))  # Update with your expected redirect URL

        user = get_user_model().objects.get(email='normal@user.com')

        profile = NormalProfile.objects.get(user=user)
        self.assertEqual(profile.normal_user_id, '12345')


class SupervisorSignUpViewTest(TestCase):

    def setUp(self):
        self.url = reverse('supervisor-signup')
        User = get_user_model()
        user = User.objects.create_superuser(email='supervisor@mail.com', password='test123456')
        self.client.login(username=user.email, password='test123456')

    def test_get_request_no_supervisor(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_request_supervisor(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_request_valid_form(self):
        data = {
            'email': 'supervisor@user.com',
            'password1': 'FooBar123456',
            'password2': 'FooBar123456',
            'supervisor_id': '12345',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('supervisor-signup'))

        user = get_user_model().objects.get(email='supervisor@user.com')

        profile = SupervisorProfile.objects.get(user=user)
        self.assertEqual(profile.supervisor_id, '12345')
