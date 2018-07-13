from django.test import TestCase
from django.contrib.auth.models import User

from pcsa_GHN.models import ghnPost, Contact
from pcsa_GHN.services import *
import json

# Credentials loaded in this manner to prevent codacy warnings
credentials = json.dumps({
    "username": "foo",
    "password": "foobar",
    "username_": "foo_",
    "password_": "foobar_"
})

credentials = json.loads(credentials)


class pcsa_GHNTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(
            username=credentials['username'],
            password=credentials['password'],
            email='foo@gmail.com')
        self.user2 = User.objects.create_superuser(
            username=credentials['username_'],
            password=credentials['password_'],
            email='foo_@gmail.com')

        self.post1 = ghnPost(
            owner=self.user1.pcuser,
            title='Title 1',
            description='Description 1')
        self.post2 = ghnPost(
            owner=self.user2.pcuser,
            title='Title 2',
            description='Description 2')
        self.post3 = ghnPost(
            owner=self.user2.pcuser,
            title='Title 3',
            description='Description 3')

        self.post1.save()
        self.post2.save()
        self.post3.save()

    def test_create_post(self):
        ghnpost = ghnPost.objects.create(
            owner=self.user1.pcuser,
            title='Some title',
            description='some description')
        ghnpost.save()
        self.assertEqual(ghnPost.objects.all().count(), 4)
        first_ghnpost = ghnPost.objects.first()
        self.assertEqual(first_ghnpost.owner.user.username, 'foo')
        self.assertEqual(first_ghnpost.owner.user.email, 'foo@gmail.com')
        self.assertEqual(first_ghnpost.title, 'Title 1')
        self.assertEqual(first_ghnpost.description, 'Description 1')

        ghnpost2 = ghnPost.objects.create(
            owner=self.user2.pcuser,
            title=self.post1.title,
            description=self.post1.description)
        ghnpost2.save()

        total_ghnposts = ghnPost.objects.all().count()
        last_ghnpost = ghnPost.objects.last()
        self.assertEqual(last_ghnpost.owner.user.username, 'foo_')
        self.assertEqual(last_ghnpost.title, self.post1.title)
        self.assertEqual(last_ghnpost.description, self.post1.description)
        self.assertEqual(total_ghnposts, 5)

        ghnpost3 = ghnPost.objects.create(
            owner=self.user2.pcuser,
            title=self.post3.title,
            description=self.post3.description)
        ghnpost3.save()

        total_ghnposts = ghnPost.objects.all().count()
        last_post = ghnPost.objects.last()
        self.assertEqual(total_ghnposts, 6)
        self.assertEqual(last_post.owner.user.username, 'foo_')
        self.assertNotEqual(last_post.owner.user.username, 'foo')
        self.assertEqual(last_post.title, self.post3.title)
        self.assertEqual(last_post.description, self.post3.description)

    def test_post_with_incorrect_info(self):
        ghnpost = ghnPost.objects.create(
            owner=self.user1.pcuser, title='', description='')

        self.assertIsNotNone(ghnpost)

        ghnpost1 = ghnPost.objects.create(
            owner=self.user2.pcuser, title='', description='')
        self.assertIsNotNone(ghnpost1)


    def test_search_post(self):
        sq = search_post(None, 'Title 1', None)

        self.assertEqual(sq.count(), 1)

        sq2 = search_post(None, 'Title 2', None)

        self.assertEqual(sq2.count(), 1)

    def test_count_of_posts(self):
        ghnpost = ghnPost(owner=self.user2.pcuser, title='Title 4',
                          description=self.post1.description)
        ghnpost2 = ghnPost(owner=self.user1.pcuser, title='Title 5',
                           description=self.post2.description)
        ghnpost3 = ghnPost(owner=self.user1.pcuser, title='Title 6',
                           description=self.post3.description)
        ghnpost.save()
        ghnpost2.save()
        ghnpost3.save()


        count = count_posts_by_pcuser('foo')

        self.assertEqual(count, 3)


""" TESTS FOR CONTACT MODEL """


class pcsa_contactTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(
            username='admin3', email='random3@gmail.com', password='password')

        self.user1.save()

        self.user2 = User.objects.create_superuser(
            username='admin4', email='random4@gmail.com', password='password')

        self.user2.save()


    def test_contact_creation(self):
        contact_1 = Contact.objects.create(
            office_name='Office 1', contact_number=1243343)
        contact_1.save()

        contact_2 = Contact.objects.create(
            office_name='Office 2', contact_number=43864856)
        contact_2.save()

        contact_3 = Contact.objects.create(
            office_name='Office 3', contact_number=9848494)
        contact_3.save()

        contact_4 = Contact.objects.create(
            office_name='Office 4', contact_number=8484040)
        contact_4.save()

        contact_5 = Contact.objects.create(
            office_name='Office 5', contact_number=88955543)
        contact_5.save()

        total_contacts = Contact.objects.all().count()

        self.assertEqual(total_contacts, 5)

        last_contact = Contact.objects.last()
        self.assertEqual(last_contact.office_name, 'Office 5')
        self.assertEqual(last_contact.contact_number, '88955543')

    def test_deleting_contact(self):
        contact_1 = Contact.objects.create(
            office_name='Office 1', contact_number=1243343)
        contact_1.save()

        contact_2 = Contact.objects.create(
            office_name='Office 2', contact_number=43864856)
        contact_2.save()

        contact_3 = Contact.objects.create(
            office_name='Office 3', contact_number=9848494)
        contact_3.save()

        contact_4 = Contact.objects.create(
            office_name='Office 4', contact_number=8484040)
        contact_4.save()

        contact_5 = Contact.objects.create(
            office_name='Office 5', contact_number=88955543)
        contact_5.save()

        total_contacts = Contact.objects.all().count()

        self.assertEqual(total_contacts, 5)

        last_contact = Contact.objects.last()
        last_contact.delete()
        total_contacts = Contact.objects.all().count()
        self.assertEqual(total_contacts, 4)

        first_contact = Contact.objects.first()
        first_contact.delete()
        total_contacts = Contact.objects.all().count()
        self.assertEqual(total_contacts, 3)

    def test_details_of_contacts(self):
        contact_1 = Contact.objects.create(
            office_name='Office 1', contact_number=1243343)
        contact_1.save()

        contact_2 = Contact.objects.create(
            office_name='Office 2', contact_number=43864856)
        contact_2.save()

        contact_3 = Contact.objects.create(
            office_name='Office 3', contact_number=9848494)
        contact_3.save()

        contact_4 = Contact.objects.create(
            office_name='Office 4', contact_number=8484040)
        contact_4.save()

        contact_5 = Contact.objects.create(
            office_name='Office 5', contact_number=88955543)
        contact_5.save()

        c = Contact.objects.get(office_name='Office 1')
        self.assertEqual(c.contact_number, '1243343')
        self.assertEqual(c.office_name, 'Office 1')
        self.assertNotEqual(c.office_name, 'Office 2')
        self.assertNotEqual(c.office_name, 'Office 3')
        self.assertNotEqual(c.contact_number, '87948049')
