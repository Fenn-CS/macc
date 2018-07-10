from django.test import TestCase
from django.contrib.auth.models import User

from pcsa_GHN.models import ghnPost, Contact
from pcsa_GHN.services import *

from signup.models import Pcuser

# Create your tests here.

class pcsa_GHNTests(TestCase):

	def setUp(self):

		self.u1 = User.objects.create_superuser(username='admin',
								password='password',
								email='random1@gmail.com'
								)
		self.u1.save()

		self.u2 = User.objects.create_superuser(username='admin2',
								password='password',
								email=''
								)
		self.u2.save()

		self.pcuser_1 = Pcuser.objects.create(user=self.u1)
		self.pcuser_1.save()

		self.pcuser_2 = Pcuser.objects.create(user=self.u2)
		self.pcuser_2.save()

		self.post_1 = ghnPost(owner=self.pcuser_1,
					title='Title 1',
					description='Description 1'
					)
		self.post_2 = ghnPost(owner=self.pcuser_2,
					title='Title 2',
					description='Description 2'
					)
		self.post_3 = ghnPost(owner=self.pcuser_2,
					title='Title 3',
					description='Description 3'
					)
		self.post_4 = ghnPost(owner=self.pcuser_1,
					title='Title 4',
					description='Description 4'
					)
		self.post_5 = ghnPost(owner=self.pcuser_1,
					title='Title 5',
					description='Description 5'
					)

		self.post_1.save()
		self.post_2.save()
		self.post_3.save()
		self.post_4.save()
		self.post_5.save()

	def test_create_post(self):

		ghnpost = ghnPost.objects.create(owner=self.pcuser_1,
						title='Some title',
						description='some description'
						)
		ghnpost.save()

		self.assertEqual(ghnPost.objects.all().count(), 6)
		first_ghnpost = ghnPost.objects.first()
		self.assertEqual(first_ghnpost.owner.user.username, 'admin')
		self.assertEqual(first_ghnpost.owner.user.email, 'random1@gmail.com')
		self.assertEqual(first_ghnpost.title, 'Title 1')
		self.assertEqual(first_ghnpost.description, 'Description 1')

		ghnpost2 = ghnPost.objects.create(owner=self.pcuser_2,
						title=self.post_1.title,
						description=self.post_1.description)
		ghnpost2.save()

		total_ghnposts = ghnPost.objects.all().count()
		last_ghnpost = ghnPost.objects.last()
		self.assertEqual(last_ghnpost.owner.user.username, 'admin2')
		self.assertEqual(last_ghnpost.title, self.post_1.title)
		self.assertEqual(last_ghnpost.description, self.post_1.description)
		self.assertEqual(total_ghnposts, 7)

		ghnpost3 = ghnPost.objects.create(owner=self.pcuser_2,
						title=self.post_3.title,
						description=self.post_3.description
						)
		ghnpost3.save()

		total_ghnposts = ghnPost.objects.all().count()
		last_post = ghnPost.objects.last()
		self.assertEqual(total_ghnposts, 8)
		self.assertEqual(last_post.owner.user.username, 'admin2')
		self.assertNotEqual(last_post.owner.user.username, 'admin')
		self.assertEqual(last_post.title, self.post_3.title)
		self.assertNotEqual(last_post.title, self.post_4.title)
		self.assertEqual(last_post.description, self.post_3.description)
		self.assertNotEqual(last_post.description, self.post_4.description)

	def test_post_with_incorrect_info(self):

		ghnpost = ghnPost.objects.create(owner=self.pcuser_1,
						title='',
						description=''
						)

		self.assertIsNotNone(ghnpost)

		ghnpost1 = ghnPost.objects.create(owner=self.pcuser_2,
						title='',
						description=''
						)
		self.assertIsNotNone(ghnpost1)

	def test_create_post_function(self):

		ghnpost = create_post(self.pcuser_1,
					self.post_1.title,
					self.post_1.description
					)
		last_post = ghnPost.objects.last()

		self.assertEqual(last_post.owner, self.pcuser_1)
		self.assertEqual(last_post.title, self.post_1.title)
		self.assertEqual(last_post.title, 'Title 1')
		self.assertEqual(last_post.description, self.post_1.description)
		self.assertEqual(last_post.description, 'Description 1')

		ghnpost2 = create_post(self.pcuser_2,
					self.post_5.title,
					self.post_5.description
					)
		first_post = ghnPost.objects.first()
		last_post = ghnPost.objects.last()

		self.assertEqual(first_post.owner, self.pcuser_1)
		self.assertEqual(first_post.title, 'Title 1')
		self.assertEqual(first_post.description, 'Description 1')
		self.assertEqual(last_post.owner, self.pcuser_2)
		self.assertEqual(last_post.title, self.post_5.title)
		self.assertEqual(last_post.title, 'Title 5')
		self.assertEqual(last_post.description, self.post_5.description)
		self.assertEqual(last_post.description, 'Description 5')

	def test_search_post(self):

		ghnpost1 = create_post(self.pcuser_1,
					self.post_1.title,
					self.post_1.description
					)

		ghnpost2 = create_post(self.pcuser_2,
					self.post_2.title,
					self.post_2.description
					)

		sq = search_post(None, 'Title 1', None)

		self.assertEqual(sq.count(), 2)

		sq2 = search_post(None, 'Title 2', None)

		self.assertEqual(sq2.count(), 2)

	def test_count_of_posts(self):

		ghnpost = create_post(self.pcuser_2,
					self.post_1.title,
					self.post_1.description
					)
		ghnpost2 = create_post(self.pcuser_1,
					self.post_2.title,
					self.post_2.description
					)
		ghnpost3 = create_post(self.pcuser_1,
					self.post_3.title,
					self.post_3.description
					)
		ghnpost4 = create_post(self.pcuser_2,
					self.post_5.title,
					self.post_5.description
					)

		count = count_posts_by_pcuser('admin')

		self.assertEqual(count, 9)


""" TESTS FOR CONTACT MODEL """

class pcsa_contactTests(TestCase):

	def setUp(self):

		self.user_1 = User.objects.create_superuser(username='admin3',
						email='random3@gmail.com',
						password='password'
						)

		self.user_1.save()

		self.user_2 = User.objects.create_superuser(username='admin4',
						email='random4@gmail.com',
						password='password'
						)

		self.user_2.save()

		self.pcuser_1 = Pcuser.objects.create(user=self.user_1)
		self.pcuser_1.save()

		self.pcuser_2 = Pcuser.objects.create(user=self.user_2)
		self.pcuser_2.save()

	
	def test_contact_creation(self):

		contact_1 = Contact.objects.create(office_name='Office 1',
						contact_number=1243343
						)
		contact_1.save()

		contact_2 = Contact.objects.create(office_name='Office 2',
						contact_number=43864856
						)
		contact_2.save()

		contact_3 = Contact.objects.create(office_name='Office 3',
						contact_number=9848494
						)
		contact_3.save()

		contact_4 = Contact.objects.create(office_name='Office 4',
						contact_number=8484040
						)
		contact_4.save()

		contact_5 = Contact.objects.create(office_name='Office 5',
						contact_number=88955543
						)
		contact_5.save()

		total_contacts = Contact.objects.all().count()

		self.assertEqual(total_contacts, 5)

		last_contact = Contact.objects.last()
		self.assertEqual(last_contact.office_name, 'Office 5')
		self.assertEqual(last_contact.contact_number, 88955543)

	def test_deleting_contact(self):

		contact_1 = Contact.objects.create(office_name='Office 1',
						contact_number=1243343
						)
		contact_1.save()

		contact_2 = Contact.objects.create(office_name='Office 2',
						contact_number=43864856
						)
		contact_2.save()

		contact_3 = Contact.objects.create(office_name='Office 3',
						contact_number=9848494
						)
		contact_3.save()

		contact_4 = Contact.objects.create(office_name='Office 4',
						contact_number=8484040
						)
		contact_4.save()

		contact_5 = Contact.objects.create(office_name='Office 5',
						contact_number=88955543
						)
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

		contact_1 = Contact.objects.create(office_name='Office 1',
						contact_number=1243343
						)
		contact_1.save()

		contact_2 = Contact.objects.create(office_name='Office 2',
						contact_number=43864856
						)
		contact_2.save()

		contact_3 = Contact.objects.create(office_name='Office 3',
						contact_number=9848494
						)
		contact_3.save()

		contact_4 = Contact.objects.create(office_name='Office 4',
						contact_number=8484040
						)
		contact_4.save()

		contact_5 = Contact.objects.create(office_name='Office 5',
						contact_number=88955543
						)
		contact_5.save()

		c = Contact.objects.get(office_name='Office 1')
		self.assertEqual(c.contact_number, 1243343)
		self.assertEqual(c.office_name, 'Office 1')
		self.assertNotEqual(c.office_name, 'Office 2')
		self.assertNotEqual(c.office_name, 'Office 3')
self.assertNotEqual(c.contact_number, 87948049 )