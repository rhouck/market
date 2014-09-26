from parse_rest.datatypes import Object
from parse_rest.user import User as ParseUser

import datetime
from django.utils.timezone import utc
from random import choice
import pyrise
import string

from settings import HIGHRISE_CONFIG, DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, LIVE

from django.core.mail import send_mail, get_connection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from inlinestyler.utils import inline_css


class Signups(Object):
    pass
class UserReferrals(Object):
    pass
class Counter(Object):
    pass
class CompanyProfiles(Object):
    pass

def get_count():

	count = Counter.Query.all()
	cur = None
	for c in count:
		cur = c
	
	return cur.count

def send_welcome_email(to_email, count, ref):

    plaintext = get_template('email_template/plain_text.txt')
    htmly     = get_template('email_template/index.html')
    d = Context({'count': count, 'ref': ref})
    subject = "Great move | BoostBlocks"
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    
    html_content = inline_css(html_content)

    connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
    if LIVE:
    	msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [to_email], [HIGHRISE_CONFIG['email']], connection=connection)
    else:
    	msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [to_email], connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def confirm_referral(ref):
	
	referrer = ParseUser.Query.all().filter(ref=ref)
	referrer = [r for r in referrer]

	if len(referrer) > 0:
		referrer = referrer[0]
		to_email = referrer.email
		# send email to referrer
		refs = UserReferrals.Query.all().filter(code=ref)

		count = int(len([r for r in refs]))

		if count < 5:
			subject = "Almost There | Exclusive discounts and priority access at BoostBlocks"
			title = "%s/5 sign-ups" % (str(int(count)))
			body = "Get 5 others to sign up to cut the line and get your first two blocks FREE. Keep sharing the link below!"
		if count == 5:
			subject = "You've earned priority access to BoostBlocks!"
			title = "You got 5 sign-ups!"
			body = "You get to cut the line and will be offered your first two blocks FREE. Keep sharing - more rewards coming soon :)"
		if count > 5:
			subject = "You are incredible"
			title = "You got %s sign-ups!" % (str(int(count)))
			body = "Wow! Those that get more sign-ups will get rewarded. You have our word."

		if count > 0:
			plaintext = get_template('email_template/counter.txt')
			htmly     = get_template('email_template/counter.html')
			d = Context({'title': title, 'body': body, 'ref': ref})

			text_content = plaintext.render(d)
			html_content = htmly.render(d)

			html_content = inline_css(html_content)

			connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
			if LIVE:
				msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [to_email], [HIGHRISE_CONFIG['email']], connection=connection)
			else:
				msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [to_email], connection=connection)
			msg.attach_alternative(html_content, "text/html")
			msg.send()

def alert_admin_new_signup(inps):
	
	subject = "New User signup"
	title = "%s has signed up" % (inps['email'])
	body =	"""Email: %s\n\nComapny: %s\n\nWebsite: %s\n\nSocial 1: %s\n\nSocial 2: %s\n\nSocial 3: %s\n\nSocial 4: %s\n\nDevelopment Stage: %s\n\nAnnual Sales: %s\n\nPitch: %s\n\nIndustry: %s\n\nTarget Description: %s\n\nBrand Description: %s\n\nClients: %s\n\nCompetition: %s\n\nOther: %s\n\nGoals: %s\n\nBudget: %s\n\nCreatives: %s\n\nWants Creatives: %s""" % (
				inps['email'],
				inps['company'],
				inps['website'],
				inps['soc_one'],
				inps['soc_two'],
				inps['soc_three'],
				inps['soc_four'],
				inps['dev_stage'],
				inps['sales'],
				inps['pitch'],
				inps['industry'],
				inps['target_description'],
				inps['brand_description'],
				inps['clients'],
				inps['competition'],
				inps['other'],
				inps['goals'],
				inps['budget'],
				inps['creatives'],
				inps['wants_creatives'],)

	plaintext = get_template('email_template/admin_com.txt')
	htmly     = get_template('email_template/admin_com.html')
	d = Context({'title': title, 'body': body,})

	text_content = plaintext.render(d)
	html_content = htmly.render(d)

	html_content = inline_css(html_content)

	connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
	if LIVE:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL], [HIGHRISE_CONFIG['email']], connection=connection)
	else:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL], connection=connection)
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def build_comp_profile(ref, inps):
	
	signup = get_signup_by_ref(ref)
	comp = CompanyProfiles(user=signup,
							company=inps['company'],
							website=inps['website'],
							soc_one=inps['soc_one'],
							soc_two=inps['soc_two'],
							soc_three=inps['soc_three'],
							soc_four=inps['soc_four'],
							dev_stage=inps['dev_stage'],
							sales=inps['sales'],
							pitch=inps['pitch'],
							industry=inps['industry'],
							target_description=inps['target_description'],
							brand_description=inps['brand_description'],
							clients=inps['clients'],
							competition=inps['competition'],
							other=inps['other'],
							goals=inps['goals'],
							budget=inps['budget'],
							creatives=inps['creatives'],
							wants_creatives=inps['wants_creatives'],
							)
	comp.save()

def bg_cust_setup(inps, count, ref, referred_by):
	
	to_email = inps['email']
	# send welcome email
	send_welcome_email(to_email, count, ref)
	build_comp_profile(ref, inps)
	alert_admin_new_signup(inps)
	
	# add referral
	if referred_by:
		signup = get_signup_by_ref(ref)	
		referral = UserReferrals(user=signup, code=referred_by,)
		referral.save()
		confirm_referral(referred_by)
	

	# increment counter
	count = Counter.Query.all()
	cur = None
	for c in count:
		cur = c
	
	try:
		cur.count += 1
		cur.save()
	except:
		pass

def gen_alphanum_key():
    key = ''
    for i in range(8):
        key += choice(string.uppercase + string.lowercase + string.digits)
    return key

def send_email(subject, body, to_email=DEFAULT_FROM_EMAIL):

	send_mail(subject, body, DEFAULT_FROM_EMAIL,[to_email], fail_silently=False)
	return True


def current_time_aware():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def get_signup_by_ref(ref):
	signup = ParseUser.Query.get(ref=str(ref))
	return signup

def get_parse_user_by_email(email):
	user = ParseUser.Query.get(email=str(email))
	return user


def create_highrise_account(email, tag=None):
	
	pyrise.Highrise.set_server(HIGHRISE_CONFIG['server'])
	pyrise.Highrise.auth(HIGHRISE_CONFIG['auth'])

	try:

		cust = pyrise.Person()

		cust.contact_data = pyrise.ContactData(email_addresses=[pyrise.EmailAddress(address=email, location='Home'),],)

		cust.first_name = email

		cust.save()
		
		cust.add_tag('boostblocks')

		if tag:
			cust.add_tag(tag)

		return cust.id
		
	except:
	    
	    return None

def parse_login(email, password):	
	
	email = email.lower()

	try:
		user = get_parse_user_by_email(email)
	except:
		return {'error': "No one has signed up with this address."}
	
	# only check for verified addresses on users who signed up after initializing email verification
	try:
		if user.emailVerified == False:
			return {'error': "Email address not verified. Please check inbox."}
	except:
		pass

	u = ParseUser.login(email, password)
	header = u.session_header()
	
	response = {'token': header['X-Parse-Session-Token']}
	response['active'] = u.active
	response['chargify_active'] = u.chargify_active
	try:
		response['ref'] = u.ref
		response['staff'] = False
	except:
		response['ref'] = None
		response['staff'] = True
		
	return response


def reset_parse_user_pass(email):
	email = email.lower()
	valid = ParseUser.request_password_reset(email=email)
	if valid:
		return True
	raise Exception("Could not send 'reset password' email.")
