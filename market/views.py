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

from parse_rest.user import User as ParseUser

def splash(request):
	
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
			signup = ParseUser.signup(email, 
										cd['password'], 
										email=email, 
										ref=ref, 
										count=count, 
										type=env_type, 
										highrise_id=highrise_id, 
										chargify_active=False, 
										staff=False)
			
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

def profile(request, ref):
	
	if not request.session['active']:
		raise Http404
	
	try:
		user = get_signup_by_ref(ref)	
	except:
		raise Http404

	acct = get_acct_details(user)

	inputs = request.POST if request.POST else None
	form = DashboardForm(inputs)
	
	
	blocks = None
	creds = None
	if (inputs) and form.is_valid():	
		cd = form.cleaned_data
		blocks = set_blocks(user, cd)
		creds = set_profile_credentials(user, cd)
	
	if not blocks:
		blocks = get_current_blocks(user)
		acct = get_acct_details(user)
		creds = acct.account_detail
	
	# re-initialize form if no post variable passed but previous block values were saved
	if blocks:
		form = DashboardForm(initial={'facebook_scale': blocks.facebook_scale, 
										'twitter_scale': blocks.twitter_scale, 
										'instagram_scale': blocks.instagram_scale,
										'facebook_profile': blocks.facebook_profile,
										'twitter_profile': blocks.twitter_profile,
										'instagram_profile': blocks.instagram_profile,
										'linkedin_profile': blocks.linkedin_profile,
										'marketing_strategy': blocks.marketing_strategy,
										'facebook_url': creds.facebook_url,
										'twitter_handle': creds.twitter_handle,
										'twitter_password': creds.twitter_password,
										'instagram_username': creds.instagram_username,
										'instagram_password': creds.instagram_password,
										})
		#return HttpResponse(str(blocks.__dict__))
	return render_to_response('profile.html', {'form': form, 'blocks': blocks, 'user': user, 'acct': acct, 'ref': ref, 'scope': 'external'}, context_instance=RequestContext(request))

	


def login(request):
	
	inputs = request.POST if request.POST else None
	form = LoginForm(inputs)
	try:
		
		if (inputs) and form.is_valid():
			
			cd = form.cleaned_data
			
			token = parse_login(cd['email'], cd['password'])
			
			if 'error' in token:
				raise Exception(token['error'])
			
			request.session['token'] = token['token']
			request.session['staff'] = token['staff']
			
			active_status = user_is_active(cd['email'])
			if 'error' in active_status:
				raise Exception(active_status['error'])
			
			request.session['active'] = active_status['status']
			
			if token['ref']:
				request.session['ref'] = token['ref']

				if request.session['active']:
					rev = str(reverse('dashboard', kwargs={'ref': token['ref']}))
				else:
					rev = str(reverse('confirmation', kwargs={'ref': token['ref']}))
				return HttpResponseRedirect(rev)

			else:
				if not request.session['active']:
					raise Exception("Your staff account has not been activated.")			
				return HttpResponseRedirect(reverse('projects'))
		else:
			raise Exception()

	except Exception as err:
		
		form.errors['__all__'] = form.error_class([err])
		return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

def resetPassword(request):
	
	inputs = request.POST if request.POST else None
	form = ResetForm(inputs)
	try:
		
		if (inputs) and form.is_valid():
			
			cd = form.cleaned_data
			
			reset_parse_user_pass(cd['email'])

			return HttpResponseRedirect(reverse('splash'))
		else:
			raise Exception()

	except Exception as err:
		
		form.errors['__all__'] = form.error_class([err])
		return render_to_response('reset.html', {'form': form}, context_instance=RequestContext(request))

def logout(request):	
	request.session.flush()
	return HttpResponseRedirect(reverse('splash'))


def createStaff(request):

	
	inputs = request.POST if request.POST else None
	form = LoginForm(inputs)
	try:
		
		if (inputs) and form.is_valid():
			
			cd = form.cleaned_data
			
			# check if email already exists
			
			existing = ParseUser.Query.all().filter(email=cd['email'])
			existing = [e for e in existing]
			if existing:
				raise Exception("Email already registered in system.")
					
			if LIVE:
				env_type = 'live'
				highrise_id = create_highrise_account(cd['email'], tag='staff')
			else:
				env_type = 'test'
				highrise_id = None

			email = cd['email'].lower()
			signup = ParseUser.signup(email, 
										cd['password'], 
										email=email, 
										type=env_type, 
										highrise_id=highrise_id, 
										chargify_active=False, 
										staff=True)
			
			user = get_parse_user_by_email(email)
			acct = AccountDetails(user_id=user.objectId, user=user, active=False)
			acct.save()

			return HttpResponseRedirect(reverse('splash'))	
			
		else:
			raise Exception()
		
	except Exception as err:
		
		form.errors['__all__'] = form.error_class([err])
		return render_to_response('create-staff.html', {'form': form}, context_instance=RequestContext(request))

def projects(request):

	if request.session['staff']:
		
		inputs = request.POST if request.POST else None

		form = UpdateAdminForm(inputs)
		
		if (inputs) and form.is_valid():
			
			try:
				cd = form.cleaned_data
				user = get_signup_by_ref(cd['ref'])
				acct = get_acct_details(user)
				#acct.account_detail.strategy = cd['strategy']
				acct.account_detail.active = cd['active']
				#acct.account_detail.goal = cd['goal']
				acct.account_detail.save()
			except:
				pass

		accts = get_accts()
		return render_to_response('projects.html', {'form': form, 'accts': accts}, context_instance=RequestContext(request))

	else:
		raise Http404		


def activate(request):
	
	inputs = request.GET if request.GET else None
	form = ActivateForm(inputs)
	try:
		
		if (inputs) and form.is_valid():
			
			if 'token' not in request.session:
				raise Exception("Session token unavailable.")
			
			cd = form.cleaned_data

			user = ParseUser.Query.all().filter(ref=cd['ref'])
			user = [u for u in user]
			if not user:
				raise Exception("User not registered in system.")
			
			user = user[0]		
			if user.chargify_active:
				raise Exception("User Chargify account already activated.")	

			user.sessionToken = request.session['token']
			user.chargify_active = True
			user.chargify_id = cd['id']
			user.save()

			rev = str(reverse('dashboard', kwargs={'ref': cd['ref']}))
			return HttpResponseRedirect(rev)	
			
		else:
			raise Exception()
		
	except Exception as err:
		form.errors['__all__'] = form.error_class([err])
		return HttpResponse(str(form.errors))
		

def company_description(request, ref):
	
	if not request.session['staff']:
		raise Http404
	
	try:
		user = get_signup_by_ref(ref)	
	except:
		raise Http404
	
	acct = None
	inputs = request.POST if request.POST else None
	
	form = CompDescForm(inputs)

	if (inputs) and form.is_valid():
		try:
			cd = form.cleaned_data
			acct = get_acct_details(user)
			acct.account_detail.storage = cd['storage']
			acct.account_detail.strategy = cd['strategy']
			acct.account_detail.goal = cd['goal']
			acct.account_detail.save()
		except:
			pass


	if not acct:
		acct = get_acct_details(user)
		form_items = {}
		for i in ('storage', 'goal', 'strategy'):
			try:
				form_items[i] = getattr(acct.account_detail, i)
			except:
				pass
		form = CompDescForm(initial=form_items)

	email = acct.user.email
	comp = acct.company_profile.__dict__

	for i in ('_created_at', '_updated_at', 'user_id', 'highrise_id', 'user', '_object_id', 'social_scale', 'ads_scale'):
		if i in comp:
			del comp[i]
	return render_to_response('comp_desc.html', {'email': email, 'comp': comp, 'ref': ref, 'scope': 'internal', 'form': form}, context_instance=RequestContext(request))
	


def test(request):
	pass
	"""
	create_acct_detail_rows()
	return render_to_response('test.html', {}, context_instance=RequestContext(request))
	"""
	

def philosophy(request):
	return render_to_response('philosophy.html', {}, context_instance=RequestContext(request))
def service(request):
	return render_to_response('service.html', {}, context_instance=RequestContext(request))
def join(request):
	return render_to_response('join.html', {}, context_instance=RequestContext(request))
def privacy(request):
	return render_to_response('priv.html', {}, context_instance=RequestContext(request))
def tos(request):
	return render_to_response('tos.html', {}, context_instance=RequestContext(request))	
