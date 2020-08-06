from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@email.com', password='123456'):
    # create sample user
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        # test tag string rep
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="comedy"
        )

        self.assertEqual(str(tag), tag.name)
