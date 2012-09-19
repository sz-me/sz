"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from sz.core.models import Message

class SimpleTest(TestCase):
    def new_ad_save(self):
		self.assertEqual(1, 1)
		
		