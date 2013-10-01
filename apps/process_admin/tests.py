"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from apps.process_admin.models import UserProfile
from django.contrib.auth.models import User


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='julian', password='barbas')
        self.userprofile = UserProfile.objects.create(dni="1085266000", user=self.user)
        self.user2 = User.objects.create_user(username='Mauricio', password='barbas')
        self.userprofile2 = UserProfile.objects.create(dni="1085266000", user=self.user2)

    def test_add(self):
    	# self.assertTrue(self.client.login(username='julian', password='barbas'))
        print UserProfile.objects.filter(dni="1085266000")
        print self.userprofile.clean()
