from django.test import TestCase
import os
from settings import *

class EnvVarsTests(TestCase):
	
	def test_django_secret_key_available(self):
		"""
		confirm configuration variables are available
		"""
		self.assertTrue(SECRET_KEY)

	def test_email_configuration_vars_are_available(self):
		"""
		confirm configuration variables are available
		"""
		self.assertTrue(EMAIL_HOST_PASSWORD)

	def test_parse_configuration_vars_are_available(self):
		"""
		confirm configuration variables are available
		"""
		self.assertTrue(PARSE_CONFIG['app_id'])
		self.assertTrue(PARSE_CONFIG['api_key'])

	def test_highrise_configuration_vars_are_available(self):
		"""
		confirm configuration variables are available
		"""
		self.assertTrue(HIGHRISE_CONFIG['auth'])
		self.assertTrue(HIGHRISE_CONFIG['email'])

from parse_rest.user import User as ParseUser
from django.core.mail import get_connection


class ApiConnectionTests(TestCase):
	
	def test_email_connection(self):
		"""
		confirm propper connection to gmail
		"""
		#connection = get_connection(username='sdsdf', password=EMAIL_HOST_PASSWORD, fail_silently=False)
		#print connection
		pass
		
	def test_parse_connection(self):
		"""
		confirm propper connection to parse
		"""
		# connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
		# trigger exception if register credentials aren't correct
		register(PARSE_CONFIG['app_id'], PARSE_CONFIG['api_key'])	
		users = [u for u in ParseUser.Query.all().limit(1)]
