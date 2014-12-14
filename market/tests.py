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
from django.core import mail
import pyrise

class ApiConnectionTests(TestCase):
	
	def test_email_connection(self):
		"""
		confirm propper connection to gmail
		"""
		mail.send_mail('subject', 'body', DEFAULT_FROM_EMAIL,['test@test.com'], fail_silently=False)
		self.assertEquals(len(mail.outbox), 1)
		self.assertEquals(mail.outbox[0].subject, 'subject')
        

	def test_parse_connection(self):
		"""
		confirm propper connection to parse
		"""
		# trigger exception if register credentials aren't correct
		raised = False
		try:
			register(PARSE_CONFIG['app_id'], PARSE_CONFIG['api_key'])	
			users = [u for u in ParseUser.Query.all().limit(1)]
		except:
			raised = True
		self.assertFalse(raised, 'Exception raised')


	def test_highrise_connection(self):
		"""
		confirm propper connection to highrise
		"""
		# trigger exception if register credentials aren't correct
		raised = False
		try:
			pyrise.Highrise.set_server(HIGHRISE_CONFIG['server'])
			pyrise.Highrise.auth(HIGHRISE_CONFIG['auth'])
			people = pyrise.Person.filter(title='manager')
		except:
			raised = True
		self.assertFalse(raised, 'Exception raised')
	

from django.core.management import call_command

class CommandTests(TestCase):
	
	def test_daily_alerts_works(self):
		raised = False
		try:
			call_command('daily_alerts', 'test')
		except:
			raised = True
		self.assertFalse(raised, 'Exception raised')

