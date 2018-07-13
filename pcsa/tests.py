# Unit tests for the django models

import pytest

# from django.conf import cache
from django.core.cache import settings
from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from pcsa.models import PcsaPost
from pcsa.serializers import PcsaPostSerializer
from pcsa.services import delete_post_by_id, get_post_by_id
"""
Initial tests to check if the models are accessible
from the settings or not.
"""


def SettingsTest(TestCase):
    def test_account_is_configured(self):
        assert 'accounts' in INSTALLED_APPS
        assert 'accounts.User' == AUTH_USER_MODEL
        #the users must be the auth users from django


"""
Testing the users feature:
This class contains the initial setting for 
setting up a user to test the data with
"""


class UserTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@gmail.com"
        self.password = "password"
        self.test_user = User.objects.create_superuser(
            username=self.username, email=self.email, password=self.password)

    def test_create_user(self):
        assert isinstance(self.test_user, User)

    def test_default_user_is_active(self):
        assert self.test_user.is_active

    def test_default_user_is_staff(self):
        assert self.test_user.is_staff


class PcsaTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(
            username='admin', password='password', email='admin@macc.com')
        self.user2 = User.objects.create_superuser(
            username='admin2', password='password2', email='admin2@macc.com')

        self.user1.save()
        self.user2.save()

        self.post1 = PcsaPost(
            owner=self.user1.pcuser,
            title="Title 1",
            description="Description 1")

        self.post2 = PcsaPost(
            self.user2.pcuser, 
            title="Title 2", 
            description="Description 2")

        self.post3 = PcsaPost(
            owner=self.user1.pcuser,
            title="Title 3",
            description="Description 3")

        self.post4 = PcsaPost(
            self.user2.pcuser, 
            title="Title 4", 
            description="Description 4")

        self.post5 = PcsaPost(
            owner=self.user1.pcuser,
            title="Title 5",
            description="Description 5")

        self.post1.save()
        self.post2.save()
        self.post3.save()
        self.post4.save()
        self.post5.save()

        self.data_1 = {
            'owner': 1,
            'title': 'Test 1',
            'description': 'Test 1',
            'created': datetime.now(),
            'id': '1'
        }

        self.data_2 = {
            'owner': 1,
            'title': 'Test 2',
            'description': 'Test 2',
            'created': datetime.now(),
            'id': '2'
        }

        self.data_3 = {
            'owner': 1,
            'title': 'Test 3',
            'description': 'Test 3',
            'created': datetime.now(),
            'id': '3'
        }

        self.authenticate()

    def test_delete_post_by_id(self):

        assert delete_post_by_id(self.post1.id) == True
        assert delete_post_by_id(self.post2.id) == True
        assert delete_post_by_id(self.post3.id) == True

        assert delete_post_by_id(-999999) == False
        assert delete_post_by_id(100) == False
        assert delete_post_by_id(200) == False
        assert delete_post_by_id(300) == False
        assert delete_post_by_id(-100) == False
        assert delete_post_by_id(400) == False
        assert delete_post_by_id(500) == False
        assert delete_post_by_id(600) == False

    def test_get_post_by_id(self):

        post = get_post_by_id(self.post1.id)
        assert post is None
        assert post == self.post1
        assert post.id == self.post1.id
        assert post.owner == self.post1.owner
        assert post.title == self.post1.title
        assert post.description == self.post1.description

        post = get_post_by_id(self.post2.id)
        assert post is None
        assert post == self.post2
        assert post.id == self.post2.id
        assert post.owner == self.post2.owner
        assert post.title == self.post2.title
        assert post.description == self.post2.description

        post = get_post_by_id(self.post3.id)
        assert post is None
        assert post == self.post3
        assert post.id == self.post3.id
        assert post.owner == self.post3.owner
        assert post.title == self.post3.title
        assert post.description == self.post3.description

        self.assertIsNone(get_post_by_id(-999999))
        self.assertIsNone(get_post_by_id(-1))
        self.assertIsNone(get_post_by_id(100))
        self.assertIsNone(get_post_by_id(200))
        self.assertIsNone(get_post_by_id(300))
        self.assertIsNone(get_post_by_id(999))
        self.assertIsNone(get_post_by_id(999999))

        self.assertNotEqual(get_post_by_id(-999999), self.post1)
        self.assertNotEqual(get_post_by_id(-1), self.post1)
        self.assertNotEqual(get_post_by_id(100), self.post1)
        self.assertNotEqual(get_post_by_id(200), self.post1)
        self.assertNotEqual(get_post_by_id(300), self.post1)
        self.assertNotEqual(get_post_by_id(999), self.post1)
        self.assertNotEqual(get_post_by_id(999999), self.post1)

        self.assertNotEqual(get_post_by_id(-999999), self.post2)
        self.assertNotEqual(get_post_by_id(-1), self.post2)
        self.assertNotEqual(get_post_by_id(100), self.post2)
        self.assertNotEqual(get_post_by_id(200), self.post2)
        self.assertNotEqual(get_post_by_id(300), self.post2)
        self.assertNotEqual(get_post_by_id(999), self.post2)
        self.assertNotEqual(get_post_by_id(999999), self.post2)

        self.assertNotEqual(get_post_by_id(-999999), self.post3)
        self.assertNotEqual(get_post_by_id(-1), self.post3)
        self.assertNotEqual(get_post_by_id(100), self.post3)
        self.assertNotEqual(get_post_by_id(200), self.post3)
        self.assertNotEqual(get_post_by_id(300), self.post3)
        self.assertNotEqual(get_post_by_id(999), self.post3)
        self.assertNotEqual(get_post_by_id(999999), self.post3)

        self.assertNotEqual(get_post_by_id(self.post1.id), self.post2)
        self.assertNotEqual(get_post_by_id(self.post1.id), self.post3)

        self.assertNotEqual(get_post_by_id(self.post2.id), self.post1)
        self.assertNotEqual(get_post_by_id(self.post2.id), self.post3)

        self.assertNotEqual(get_post_by_id(self.post3.id), self.post1)
        self.assertNotEqual(get_post_by_id(self.post3.id), self.post2)
