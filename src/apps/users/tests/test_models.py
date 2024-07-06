from django.test import TestCase

from apps.users.models.users import User


class UserCreationTestCase(TestCase):
    """
    ./manage.py test apps.users.tests.test_models.UserCreationTestCase --settings=_dev.settings_test        # flake8: noqa
    """

    def test_create_user(self):
        email = "user@user.com"
        User.objects.create_user(email=email, password="P@$$w0rd", is_verified=True, is_active=True)
        user = list(User.objects.filter(email=email).all())
        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].email, email)
        self.assertTrue(user[0].is_verified)
        self.assertTrue(user[0].is_active)
        self.assertFalse(user[0].is_superuser)

    def test_create_superuser(self):
        email = "superuser@user.com"
        User.objects.create_superuser(
            email=email, password="P@$$w0rd", is_verified=True, is_active=True
        )
        user = list(User.objects.filter(email=email).all())
        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].email, email)
        self.assertTrue(user[0].is_verified)
        self.assertTrue(user[0].is_active)
        self.assertTrue(user[0].is_superuser)
