from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        # Test creating a new user with an email is successful
        email = 'test@email.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # testing if new user email is normalized
        email = 'test@EMAIL.com'
        user = get_user_model().objects.create_user(email, 'TestPass123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # test creating user with no email raises error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'TestPass123')

    def test_create_new_superuser(self):
        # test creating super user
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'TestPass123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
