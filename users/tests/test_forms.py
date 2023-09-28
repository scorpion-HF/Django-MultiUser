from django.test import TestCase
from users.forms import NormalUserSignUpForm, SupervisorSignUpForm
from users.models import NormalProfile, SupervisorProfile


class SignUpFormTest(TestCase):
    def test_normal_form_valid_data(self):
        data = {
            'email': 'normal@user.com',
            'password1': 'FooBar123456',
            'password2': 'FooBar123456',
            'normal_user_id': '12345',
        }
        form = NormalUserSignUpForm(data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.email, 'normal@user.com')
        self.assertFalse(user.is_supervisor)
        self.assertTrue(user.is_normal)

        profile = NormalProfile.objects.get(user=user)
        self.assertEqual(profile.normal_user_id, '12345')

    def test_normal_form_invalid_data(self):
        data = {
            'email': 'invalidemail',
            'password1': 'FooBar123456',
            'password2': 'FooBar123456',
            'normal_user_id': '',
        }
        form = NormalUserSignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('normal_user_id', form.errors)

    def test_supervisor_form_valid_data(self):
        data = {
            'email': 'supervisor@user.com',
            'password1': 'FooBar123456',
            'password2': 'FooBar123456',
            'supervisor_id': '54321',
        }
        form = SupervisorSignUpForm(data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.email, 'supervisor@user.com')
        self.assertTrue(user.is_supervisor)
        self.assertFalse(user.is_normal)

        profile = SupervisorProfile.objects.get(user=user)
        self.assertEqual(profile.supervisor_id, '54321')

    def test_supervisor_form_invalid_data(self):
        data = {
            'email': 'invalidemail',
            'password1': 'FooBar123456',
            'password2': 'FooBar123456',
            'supervisor_id': '',
        }
        form = SupervisorSignUpForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('supervisor_id', form.errors)
