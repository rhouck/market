from parse_rest.datatypes import Object
from parse_rest.user import User as ParseUser

import datetime
from django.utils.timezone import utc
from random import choice
import pyrise
import string

from settings import HIGHRISE_CONFIG, DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, LIVE

from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from inlinestyler.utils import inline_css

import django_rq
redis_conn = django_rq.get_connection()

class UserReferrals(Object):
    pass
class Counter(Object):
    pass
class CompanyProfiles(Object):
    pass
class AccountDetails(Object):
    pass
class SelectedBlocks(Object):
    pass
class ProfileBuilder(Object):
    pass

class Account(object):
    """
    This object contains all relvant information to an individual user and his/her associated company information.

    Attributes:
        user: The Parse User object.
        account_detail: The Parse AccountDetails object.
        company_profile: The Parse CompanyProfiles Object.
    """
    def __init__(self):
    	self.user = None
    	self.account_detail = None
    	self.company_profile = None

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

def confirmed_payments_email(acct):

	subject = "New customer payment information received"
	title = "New customer payment information received"
	body = "Email: %s\n\n" % (acct.user.email)
	try:
		body += "Name: %s\n\n" % (acct.user.full_name)
	except:
		pass
	body += "Company: %s\n\n" % (acct.company_profile.company)

	plaintext = get_template('email_template/admin_com.txt')
	htmly     = get_template('email_template/admin_com.html')
	d = Context({'title': title, 'body': body,})

	text_content = plaintext.render(d)
	html_content = htmly.render(d)

	html_content = inline_css(html_content)

	connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
	if LIVE:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL, 'ryan@boostblocks.com','sarina@boostblocks.com'], [HIGHRISE_CONFIG['email']], connection=connection)
	else:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL,], connection=connection)
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

		if count < 3:
			subject = "Almost There | Priority access at BoostBlocks"
			title = "%s/3 sign-ups" % (str(int(count)))
			body = "Get 3 others to sign up to cut the line. Keep sharing the link below!"
		if count == 3:
			subject = "You've earned priority access to BoostBlocks!"
			title = "You got 3 sign-ups!"
			body = "You get to cut the line. Keep sharing - more rewards coming soon :)"
		if count > 3:
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
	
	body = ""
	for k in inps.iterkeys():
		body += "%s: %s\n\n" % (k, inps[k])

	plaintext = get_template('email_template/admin_com.txt')
	htmly     = get_template('email_template/admin_com.html')
	d = Context({'title': title, 'body': body,})

	text_content = plaintext.render(d)
	html_content = htmly.render(d)

	html_content = inline_css(html_content)

	connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
	if LIVE:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL, 'ryan@boostblocks.com','sarina@boostblocks.com'], [HIGHRISE_CONFIG['email']], connection=connection)
	else:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL, 'ryan@boostblocks.com'], connection=connection)
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def build_comp_profile(ref, inps):
	
	signup = get_signup_by_ref(ref)

	acct = AccountDetails(user_id=signup.objectId, user=signup, active=False, promo=inps['promo'], chargify_active=False, blocks_enabled=False, hidden=False,)
	acct.save()

	comp = CompanyProfiles(user=signup, user_id=signup.objectId)
	
	for k in inps.iterkeys():
		setattr(comp, k, inps[k])
	"""
							
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
	"""
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
	email = email.lower()
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
			if isinstance(tag, list):
				for t in tag:
					cust.add_tag(t)
			else:
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
	
	response = {'token': header['X-Parse-Session-Token'],
				}
				#'chargify_active': u.chargify_active,
				#'active': u.active,
				#'user': u,
	
	try:
		response['ref'] = u.ref
		response['staff'] = False
	except:
		response['ref'] = None
		response['staff'] = True
		
	return response



def get_acct_details(user):
	
	# accepts either user object or user object ID
	try:
		test = user.objectId 
	except:
		user = ParseUser.Query.get(objectId=str(user))

	account = Account()
	account.user = user

	user_id = user.objectId
	try:
		acct = AccountDetails.Query.get(user_id=user_id)
		account.account_detail = acct
	except:
		pass

	try:
		comp_profile = CompanyProfiles.Query.get(user_id=user_id)
		account.company_profile = comp_profile
	except:
		pass

	return account
	
def get_accts(show_hidden=False):

	
	if not show_hidden:
		accts = AccountDetails.Query.filter(hidden=False)
	else:
		accts = AccountDetails.Query.all()
	
	accts = [get_acct_details(a.user_id) for a in accts if not a.user['staff']]
	
	accts_blocks = []
	for a in accts:
		if a.account_detail.chargify_active:
			a.blocks = get_current_blocks(a.user)
		else:
			a.blocks = None
		accts_blocks.append(a)
	return accts_blocks


def user_is_active(email):
	user = get_parse_user_by_email(email)
	try:
		acct = get_acct_details(user)
		return {'status': acct.account_detail.active}
	except Exception as err:
		return {'error': "No record found for user with that email address: %s" % (str(err))}	


def reset_parse_user_pass(email):
	email = email.lower()
	valid = ParseUser.request_password_reset(email=email)
	if valid:
		return True
	raise Exception("Could not send 'reset password' email.")


def set_blocks(user, form):
	
	# if no blocks have previosly been requested and this set has zero values across board, don't record it
	blocks = SelectedBlocks.Query.filter(user_id=user.objectId)
	blocks = [b for b in blocks]
	count = sum([int(form[i]) for i in ('facebook_scale', 'twitter_scale', 'instagram_scale')])
	if len(blocks) == 0 and count == 0:
		return True

	# send email if this is first time blocks were purchased
	if len(blocks) == 0 and count != 0:
		result = django_rq.enqueue(check_first_blocks, user, form)

	# update scale of boost blocks
	blocks = SelectedBlocks(user=user, 
							user_id=user.objectId,
							#facebook_profile=form['facebook_profile'],
							#twitter_profile=form['twitter_profile'],
							#instagram_profile=form['instagram_profile'],
							#marketing_strategy=form['marketing_strategy'],
							#linkedin_profile=form['linkedin_profile'],
							facebook_scale=int(form['facebook_scale']),
							twitter_scale=int(form['twitter_scale']),
							instagram_scale=int(form['instagram_scale']),
							)
	blocks.save()
	
	return blocks

def check_first_blocks(user, form):

	# send email to boost blocks team if this is first time user has selected blocks
	subject = "First time Boost Blocks ordered"
	title = "First time Boost Blocks ordered"

	body = "Email: %s\n" % (user.email)
	try:
		body += "Name: %s\n" % (user.full_name)
	except:
		pass
	try:
		company = CompanyProfiles.Query.get(user_id=str(user.objectId))
		body += "Company: %s\n" % (company.company)
	except:
		pass

	for i in ('facebook_scale', 'twitter_scale', 'instagram_scale'):
		body += "%s - set to: %s\n" % (i, form[i])
	body += "\n\n"
	
	plaintext = get_template('email_template/admin_com.txt')
	htmly     = get_template('email_template/admin_com.html')
	d = Context({'title': title, 'body': body,})

	text_content = plaintext.render(d)
	html_content = htmly.render(d)

	html_content = inline_css(html_content)

	connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
	if LIVE:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL, 'ryan@boostblocks.com','sarina@boostblocks.com'], [HIGHRISE_CONFIG['email']], connection=connection)
	else:
		msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL,], connection=connection)
	msg.attach_alternative(html_content, "text/html")
	msg.send()





def record_profile_builder(user, form):
	# record request for profile builder blocks if exist
	if form['facebook_profile'] or form['twitter_profile'] or form['instagram_profile'] or form['marketing_strategy'] or form['linkedin_profile']:
		builder = ProfileBuilder(user=user, 
								user_id=user.objectId,
								facebook_profile=form['facebook_profile'],
								twitter_profile=form['twitter_profile'],
								instagram_profile=form['instagram_profile'],
								marketing_strategy=form['marketing_strategy'],
								linkedin_profile=form['linkedin_profile'],
								)
		builder.save()
	return True

def get_current_blocks(user):
	
	try:
		test = user.objectId 
	except:
		user = ParseUser.Query.get(objectId=str(user))

	acct = AccountDetails.Query.get(user_id=user.objectId)
	
	blocks_set = {'per_end': None, 'latest': None, 'current': None, 'change': None}
	if not acct.chargify_active:
		return blocks_set

	per_end = acct.chargify_per_end
	last_per_end = per_end - datetime.timedelta(days=7)
	
	blocks_set['per_end'] = per_end

	for i in (('latest', datetime.datetime(3000,1,1,0,0)), ('current', last_per_end)):
		blocks = SelectedBlocks.Query.filter(user_id=user.objectId, createdAt__lte=i[1]).order_by("-createdAt")
		blocks = [b for b in blocks]
		if blocks:
			blocks_set[i[0]] = blocks[0]
		else:
			blocks_set[i[0]] = None
	
	# show changes to block selection from prior period
	if blocks_set['latest'] and blocks_set['current']:
		blocks_set['change'] = {}
		for i in ('facebook_scale', 'twitter_scale', 'instagram_scale'):
			blocks_set['change'][i] = getattr(blocks_set['latest'], i) - getattr(blocks_set['current'], i)

	return blocks_set

def get_recent_profile_builders(user):
	now = current_time_aware()
	week_ago = now - datetime.timedelta(days=7)
	builders = ProfileBuilder.Query.filter(user_id=user.objectId, createdAt__gte=week_ago).order_by("createdAt")
	builders_list = []
	
	for b in builders:
		for i in ('facebook_profile', 'twitter_profile', 'instagram_profile', 'marketing_strategy', 'linkedin_profile'): 
			if getattr(b, i):
				split = i.split('_')
				name = ""
				for s in split:
					name += "%s " % (s.title())
				builders_list.append((name, b.createdAt))
	return builders_list
			

	

def set_profile_credentials(user, form):
	acct = AccountDetails.Query.get(user_id=user.objectId)	
	for i in ('facebook_url','twitter_handle','twitter_password','instagram_username','instagram_password',):
		setattr(acct, i, form[i])
	acct.save()
	return acct



"""
These functions send email notification of customer activity to be scheduled in cron jobs
"""
def profile_builder_alert_email():

	now = current_time_aware()
	yesterday = now - datetime.timedelta(days=1)

	builder = ProfileBuilder.Query.filter(createdAt__gte=yesterday)
	if LIVE:
		builder = [b for b in builder if b.user['type'] == 'live']
	else:
		builder = [b for b in builder]

	if builder:
			
		subject = "New profile builder blocks ordered"
		title = "New profile builder blocks ordered"
		body = ""

		for b in builder:

			body += "Email: %s\n" % (b.user['email'])
			try:
				body += "Name: %s\n" % (b.user['full_name'])
			except:
				pass
			try:
				company = CompanyProfiles.Query.get(user_id=str(b.user_id))
				body += "Company: %s\n" % (company.company)
			except:
				pass

			for i in ('facebook_profile', 'twitter_profile', 'instagram_profile', 'marketing_strategy', 'linkedin_profile'): 
					if getattr(b, i):
						split = i.split('_')
						name = ""
						for s in split:
							name += "%s " % (s.title())
						body += "%s\n" % (name)
			body += "\n\n\n"
			
		
		plaintext = get_template('email_template/admin_com.txt')
		htmly     = get_template('email_template/admin_com.html')
		d = Context({'title': title, 'body': body,})

		text_content = plaintext.render(d)
		html_content = htmly.render(d)

		html_content = inline_css(html_content)

		connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
		if LIVE:
			msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL, 'ryan@boostblocks.com','sarina@boostblocks.com'], [HIGHRISE_CONFIG['email']], connection=connection)
		else:
			msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL,], connection=connection)
		msg.attach_alternative(html_content, "text/html")
		msg.send()

def check_block_updates():
	
	now = current_time_aware()
	subject = title = "Updates to customer blocks"
	body = ""

	def build_email_body_by_date(accts, update_per_end=False):
		body = ""
		for a in accts:
			user = get_parse_user_by_email(a.user['email'])
			blocks = get_current_blocks(user)
			if blocks['latest']:
				body += "Email: %s\n" % (user.email)
				try:
					body += "Name: %s\n" % (user['full_name'])
				except:
					pass
				try:
					company = CompanyProfiles.Query.get(user_id=str(a.user_id))
					body += "Company: %s\n" % (company.company)
				except:
					pass

				for i in ('facebook_scale', 'twitter_scale', 'instagram_scale'):
					body += "%s - set to: %s" % (i, getattr(blocks['latest'],i))
					try:
						body +=  " (change from last period: %s)" % (blocks['change'][i])
					except:
						pass
					body += "\n"
				body += "\n\n"
		
			if update_per_end:
				# update billing period end
				a.chargify_per_end += datetime.timedelta(days=7)
				a.save()	
		
		return body	

	def filter_accts(LIVE, accts):
		if LIVE:
			accts = [a for a in accts if a.user['type'] == 'live']
		else:
			accts = [a for a in accts]
		return accts

	# update billing period and show updates to blocks
	accts = AccountDetails.Query.filter(chargify_active=True, chargify_per_end__lte=now)
	accts = filter_accts(LIVE, accts)
	if accts:
		body += "Today's block updates:\n\n"
		body += build_email_body_by_date(accts, update_per_end=True)
		body += "\n\n\n"		
		
	# show expected updates to blocks
	accts = AccountDetails.Query.filter(chargify_active=True, chargify_per_end__lte=(now+datetime.timedelta(days=1)), chargify_per_end__gte=now)
	accts = filter_accts(LIVE, accts)
	if accts:
		body += "Tomorrow's expected block updates:\n\n"
		body += build_email_body_by_date(accts)
		body += "\n\n\n"

	accts = AccountDetails.Query.filter(chargify_active=True, chargify_per_end__lte=(now+datetime.timedelta(days=2)), chargify_per_end__gte=(now+datetime.timedelta(days=1)))
	accts = filter_accts(LIVE, accts)
	if accts:
		body += "Day after tomorrow's expected block updates:\n\n"
		body += build_email_body_by_date(accts)
		body += "\n\n\n"		

	if body:
		plaintext = get_template('email_template/admin_com.txt')
		htmly     = get_template('email_template/admin_com.html')
		d = Context({'title': title, 'body': body,})

		text_content = plaintext.render(d)
		html_content = htmly.render(d)

		html_content = inline_css(html_content)

		connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
		if LIVE:
			msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL, 'ryan@boostblocks.com','sarina@boostblocks.com'], [HIGHRISE_CONFIG['email']], connection=connection)
		else:
			msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL,], connection=connection)
		msg.attach_alternative(html_content, "text/html")
		msg.send()


def daily_work(test=False):
	if not test:
		result = django_rq.enqueue(profile_builder_alert_email)
		result = django_rq.enqueue(check_block_updates)
	return True

	