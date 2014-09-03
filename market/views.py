from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout
from django.contrib.auth.views import login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.forms.util import ErrorList

import datetime
import json
import ast
from dateutil.parser import parse


from forms import *
from settings import LIVE

from utils import *


import django_rq
redis_conn = django_rq.get_connection()
"""
from rq import Queue
from worker import conn
q = Queue(connection=conn)
"""
from parse_rest.user import User as ParseUser

def splash(request):
	"""
	# get referral code if exists
	inputs = request.GET if request.GET else None
	form = ReferralForm(inputs)
	referred_by = None
	if (inputs) and form.is_valid():
		cd = form.cleaned_data
		referred_by = cd['ref']
	
	
	inputs = request.POST if request.POST else None
	form = SubscribeForm(inputs)
	try:
		
		if (inputs) and form.is_valid():
			
			cd = form.cleaned_data
			
			# check if email already exists
			existing = Signups.Query.all().filter(email=cd['email'])
			existing = [e for e in existing]
			if existing:
				raise Exception("Email already registered in system.")
			
			# get user count
			count = get_count()

			# create user
			ref = gen_alphanum_key()
			signup = Signups(email=cd['email'], ref=ref, count=count)
			if LIVE:
				signup.type = 'live'
				signup.highrise_id = create_highrise_account(cd['email'], tag='landing-page')
			else:
				signup.type = 'test'
			signup.save()
			
			result = django_rq.enqueue(bg_cust_setup, cd['email'], count, ref, referred_by)
			#result = q.enqueue(bg_cust_setup, cd['email'], count, ref, referred_by)
			rev = str(reverse('confirmation', kwargs={'ref': ref}))
			return HttpResponseRedirect(rev)	
			
			
			# submit contact form
			elif inputs['type'] == 'Contact' and con_form.is_valid():	
				
				cd = con_form.cleaned_data
				body = "%s:\n\n%s" % (cd['email'],cd['message'])
				send_email(subject='Inquiry from site', body=body)
				create_highrise_account(cd['email'], tag='contact-form')
				
				return HttpResponseRedirect(reverse('confirmation', kwargs={'message_type': 'contact'}))
				
		else:
			raise Exception()

		
	except Exception as err:
		
		form.errors['__all__'] = form.error_class([err])
		return render_to_response('splash.html', {'form': form}, context_instance=RequestContext(request))
	"""
	return render_to_response('splash.html', {}, context_instance=RequestContext(request))

def signup(request):

	# get referral code if exists
	inputs = request.GET if request.GET else None
	form = ReferralForm(inputs)
	referred_by = None
	if (inputs) and form.is_valid():
		cd = form.cleaned_data
		referred_by = cd['ref']


	inputs = request.POST if request.POST else None
	form = SubscribeForm(inputs)
	try:
		
		if (inputs) and form.is_valid():
			
			cd = form.cleaned_data
			
			# check if email already exists
			
			existing = ParseUser.Query.all().filter(email=cd['email'])
			existing = [e for e in existing]
			if existing:
				raise Exception("Email already registered in system.")
					
			# get user count
			count = get_count()

			# create user
			ref = gen_alphanum_key()
			if LIVE:
				env_type = 'live'
				highrise_id = create_highrise_account(cd['email'], tag='signup')
			else:
				env_type = 'test'
				highrise_id = None

			email = cd['email'].lower()
			signup = ParseUser.signup(email, cd['password'], email=email, ref=ref, count=count, type=env_type, highrise_id=highrise_id)
			
			result = django_rq.enqueue(bg_cust_setup, cd, count, ref, referred_by)
			
			rev = str(reverse('confirmation', kwargs={'ref': ref}))
			return HttpResponseRedirect(rev)	
			"""
			url = "https://surprisr.chargify.com/h/3537446/subscriptions/new"
			if referred_by:
				url += "?ref=%s" % (referred_by)
			return HttpResponseRedirect(url)	
			"""
			
		else:
			raise Exception()

		
	except Exception as err:
		
		form.errors['__all__'] = form.error_class([err])
		return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))
	


def confirmation(request, ref):
	try:
		signup = get_signup_by_ref(ref)	
		return render_to_response('confirmation.html', {'ref': ref, 'count': signup.count}, context_instance=RequestContext(request))
	except:
		raise Http404

def gifts(request):
	return render_to_response('gifts.html', {}, context_instance=RequestContext(request))
def privacy(request):
	return render_to_response('priv.html', {}, context_instance=RequestContext(request))
def tos(request):
	return render_to_response('tos.html', {}, context_instance=RequestContext(request))	
