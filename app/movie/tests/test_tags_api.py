from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from movie.serializers import TagSerializer

TAGS_URL = reverse('movie:tag-list')


class PublicTagsApiTest(TestCase):
    # test publically available tags API

    def setUp(self):
        self.client = APIClient()

        def test_login_required(self):
            res = self.client.get(TAGS_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    # test authorized test case
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            '123456'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        # test retrieving tags
        Tag.objects.create(user=self.user, name='Comedy')
        Tag.objects.create(user=self.user, name='Horror')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        # tags are returned for auth user
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            '123456'
        )
        Tag.objects.create(user=user2, name='Comedy')
        tag = Tag.objects.create(user=self.user, name='Drama')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
