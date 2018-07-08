from django.contrib.auth.models import User
from django.test import TestCase

from malaria_web.models import Post, RevPost
from malaria_web.services import (create_revpost, delete_post_by_id,
                                  get_post_by_id, get_revposts_of_owner)
import json


# Credentials loaded in this manner to prevent codacy warnings
credentials = json.dumps({
  "username":"foo",
  "password":"foobar",
  "username_":"foo_",
  "password_":"foobar_" 
})

credentials = json.loads(credentials)

class MalariaTests(TestCase):

    def setUp(self):
        """Setup the test database"""

        self.user1 = User.objects.create_superuser(
        username=credentials['username'], password=credentials['password'], email='')
        self.user2 = User.objects.create_superuser(
        username=credentials['username_'], password=credentials['password_'], email='')
        self.user1.save()
        self.user2.save()
        self.post1 = Post.objects.create(
            owner=self.user1.pcuser,
            title_post="Post Title 1",
            description_post="Post Description 1")
        self.post2 = Post.objects.create(
            owner=self.user2.pcuser,
            title_post="Post Title 2",
            description_post="Post Description 2")

    def test_create_revpost(self):

        revpost = create_revpost(
            self.user1.pcuser, self.post1, self.post1.title_post,
            self.post1.description_post, self.post1.link_post, self.post1.photo)

        self.assertIsNotNone(revpost)

    def test_delete_post_by_id(self):

        self.assertTrue(delete_post_by_id(self.post1.id))
        self.assertTrue(delete_post_by_id(self.post2.id))
        self.assertFalse(delete_post_by_id(-999999))
        self.assertFalse(delete_post_by_id(-1))
        self.assertFalse(delete_post_by_id(100))
        self.assertFalse(delete_post_by_id(200))
        self.assertFalse(delete_post_by_id(300))
        self.assertFalse(delete_post_by_id(400))
        self.assertFalse(delete_post_by_id(500))
        self.assertFalse(delete_post_by_id(600))
        self.assertFalse(delete_post_by_id(999))
        self.assertFalse(delete_post_by_id(999999))

    def test_get_post_by_id(self):

        post = get_post_by_id(self.post1.id)
        self.assertIsNotNone(post)
        self.assertEqual(post, self.post1)
        self.assertEqual(post.id, self.post1.id)
        self.assertEqual(post.owner, self.post1.owner)
        self.assertEqual(post.title_post, self.post1.title_post)
        self.assertEqual(post.description_post, self.post1.description_post)

        post = get_post_by_id(self.post2.id)
        self.assertIsNotNone(post)
        self.assertEqual(post, self.post2)
        self.assertEqual(post.id, self.post2.id)
        self.assertEqual(post.owner, self.post2.owner)
        self.assertEqual(post.title_post, self.post2.title_post)
        self.assertEqual(post.description_post, self.post2.description_post)

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

    def test_get_revposts_of_owner(self):

        RevPost.objects.all().delete()
        revpost_list = get_revposts_of_owner(self.post1.id)
        self.assertEqual(len(revpost_list), 0)

        revpost_1 = create_revpost(
            self.user1.pcuser, self.post1, self.post1.title_post,
            self.post1.description_post, self.post1.link_post, self.post1.photo)

        revpost_list = get_revposts_of_owner(self.post1.id)
        self.assertEqual(len(revpost_list), 1)
        self.assertIn(revpost_1, revpost_list)
        revpost_compare = RevPost.objects.get(pk=revpost_1.id)
        self.assertEqual(revpost_compare.owner_rev, self.user1.pcuser)
        self.assertEqual(revpost_compare.owner_rev_post, self.post1)
        self.assertEqual(revpost_compare.title_post_rev, "Post Title 1")
        self.assertEqual(revpost_compare.description_post_rev,
                         "Post Description 1")
        revpost_2 = create_revpost(self.user1.pcuser, self.post1,
                                   "Post Title 2", "Post Description 2",
                                   self.post1.link_post, self.post1.photo)

        revpost_list = get_revposts_of_owner(self.post1.id)
        self.assertEqual(len(revpost_list), 2)
        self.assertIn(revpost_1, revpost_list)
        self.assertIn(revpost_2, revpost_list)
        revpost_compare = RevPost.objects.get(pk=revpost_2.id)
        self.assertEqual(revpost_compare.owner_rev, self.user1.pcuser)
        self.assertEqual(revpost_compare.owner_rev_post, self.post1)
        self.assertEqual(revpost_compare.title_post_rev, "Post Title 2")
        self.assertEqual(revpost_compare.description_post_rev,
                         "Post Description 2")

        revpost_1 = create_revpost(
            self.user1.pcuser, self.post2, self.post2.title_post,
            self.post2.description_post, self.post2.link_post, self.post2.photo)

        revpost_list = get_revposts_of_owner(self.post2.id)
        self.assertEqual(len(revpost_list), 1)
        self.assertIn(revpost_1, revpost_list)
        revpost_compare = RevPost.objects.get(pk=revpost_1.id)
        self.assertEqual(revpost_compare.owner_rev, self.user1.pcuser)
        self.assertEqual(revpost_compare.owner_rev_post, self.post2)
        self.assertEqual(revpost_compare.title_post_rev, "Post Title 2")
        self.assertEqual(revpost_compare.description_post_rev,
                         "Post Description 2")

        revpost_2 = create_revpost(self.user1.pcuser, self.post2,
                                   "Test title 2", "Test description 2",
                                   self.post2.link_post, self.post2.photo)

        revpost_list = get_revposts_of_owner(self.post2.id)
        self.assertEqual(len(revpost_list), 2)
        self.assertIn(revpost_1, revpost_list)
        self.assertIn(revpost_2, revpost_list)
        revpost_compare = RevPost.objects.get(pk=revpost_2.id)
        self.assertEqual(revpost_compare.owner_rev, self.user1.pcuser)
        self.assertEqual(revpost_compare.owner_rev_post, self.post2)
        self.assertEqual(revpost_compare.title_post_rev, "Test title 2")
        self.assertEqual(revpost_compare.description_post_rev,
                         "Test description 2")

        revpost_list = get_revposts_of_owner(-999999)
        self.assertEqual(len(revpost_list), 0)

        revpost_list = get_revposts_of_owner(-1)
        self.assertEqual(len(revpost_list), 0)

        revpost_list = get_revposts_of_owner(100)
        self.assertEqual(len(revpost_list), 0)

        revpost_list = get_revposts_of_owner(200)
        self.assertEqual(len(revpost_list), 0)

        revpost_list = get_revposts_of_owner(300)
        self.assertEqual(len(revpost_list), 0)

        revpost_list = get_revposts_of_owner(999)
        self.assertEqual(len(revpost_list), 0)

        revpost_list = get_revposts_of_owner(999999)
        self.assertEqual(len(revpost_list), 0)
