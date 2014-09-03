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
class Recipients(Object):
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
    subject = "Great move | Surprisr"
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
			subject = "Almost There | Exclusive discounts and priority access at Surprisr"
			title = "%s/5 sign-ups" % (str(int(count)))
			body = "Get 5 of your friends to sign up to cut the line and get exclusive discounts on your first gifts. Keep sharing the link below!"
		if count == 5:
			subject = "You've earned priority access to Surprisr!"
			title = "You got 5 sign-ups!"
			body = "You get to cut the line and will be offered exclusive discounts on your first gifts at Surprisr. Keep sharing - more rewards coming soon :)"
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

def recipient_demographics(ref, inps):
	
	signup = get_signup_by_ref(ref)
	recipient = Recipients(user=signup,
							age=inps['age'],
							style=inps['style'],
							soc_one=inps['soc_one'],
							soc_two=inps['soc_two'],
							)
	recipient.save()

def bg_cust_setup(inps, count, ref, referred_by):
	
	to_email = inps['email']
	# send welcome email
	send_welcome_email(to_email, count, ref)
	recipient_demographics(ref, inps)
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
		
		if tag:
			cust.add_tag(tag)

		return cust.id
		
	except:
	    
	    return None

