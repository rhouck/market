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
			"""
			existing = ParseUser.Query.all().filter(email=cd['email'])
			existing = [e for e in existing]
			if existing:
				raise Exception("Email already registered in system.")
			"""
			try:
				existing = get_parse_user_by_email(cd['email'])		
				raise Exception("Email already registered in system.")
			except:
				pass

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
										full_name=cd['full_name'],
										ref=ref, 
										count=count, 
										type=env_type, 
										highrise_id=highrise_id, 
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

	inputs = request.POST if request.POST else None
	form = DashboardForm(inputs)
	
	if (inputs) and form.is_valid():	
		cd = form.cleaned_data
		form_type = inputs['type']
		if form_type != 'builder':
			set_profile_credentials(user, cd)
			if form_type == 'blocks':
				set_blocks(user, cd)
		else:
			record_profile_builder(user, cd)

	acct = get_acct_details(user)
	builders = get_recent_profile_builders(user)
	blocks = get_current_blocks(user)
	
	initial = {'facebook_url': acct.account_detail.facebook_url,
				'twitter_handle': acct.account_detail.twitter_handle,
				'twitter_password': acct.account_detail.twitter_password,
				'instagram_username': acct.account_detail.instagram_username,
				'instagram_password': acct.account_detail.instagram_password,
				}
	if blocks['latest']:
		initial.update({'facebook_scale': blocks['latest'].facebook_scale, 
						'twitter_scale': blocks['latest'].twitter_scale, 
						'instagram_scale': blocks['latest'].instagram_scale,})
	form = DashboardForm(initial=initial)

	return render_to_response('profile.html', {'form': form, 'blocks': blocks, 'acct': acct, 'ref': ref, 'scope': 'external', 'builders': builders}, context_instance=RequestContext(request))

	


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
			cd = form.cleaned_data
			
			try:	
				user = get_signup_by_ref(cd['ref'])
				acct = get_acct_details(user)
				#acct.account_detail.strategy = cd['strategy']
				acct.account_detail.active = cd['active']
				acct.account_detail.blocks_enabled = cd['blocks_enabled']
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
			"""
			user = ParseUser.Query.all().filter(ref=cd['ref'])
			user = [u for u in user]
			if not user:
				raise Exception("User not registered in system.")
			user = user[0]
			"""
			try:
				user = get_signup_by_ref(cd['ref'])
			except:
				raise Exception("User not registered in system.")

			acct = get_acct_details(user)

			if acct.account_detail.chargify_active:
				raise Exception("User Chargify account already activated.")	

			acct.user.sessionToken = request.session['token']
			acct.user.chargify_id = cd['id']
			acct.user.save()
			acct.account_detail.chargify_active = True
			acct.account_detail.chargify_per_end = current_time_aware() + datetime.timedelta(days=7)
			acct.account_detail.save()

			result = django_rq.enqueue(confirmed_payments_email, acct)

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
	result = django_rq.enqueue(profile_builder_alert_email)
	return HttpResponse(True)

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
