from django.contrib.auth import get_user_model
from django.test import TestCase
from users.models import NormalProfile, SupervisorProfile


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_supervisor)
        self.assertFalse(user.is_normal)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)


class ProfileTestCase(TestCase):

    def test_normal_profile(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        profile = NormalProfile.objects.create(user=user, normal_user_id=123)
        self.assertEqual(profile.normal_user_id, 123)
        self.assertEqual(profile.user, user)

    def test_supervisor_profile(self):
        User = get_user_model()
        user = User.objects.create_user(email="supervisor@user.com", password="foo")
        profile = SupervisorProfile.objects.create(user=user, supervisor_id=123)
        self.assertEqual(profile.supervisor_id, 123)
        self.assertEqual(profile.user, user)
