from django import forms
from django.forms import widgets
from tinymce.widgets import TinyMCE

class ResetForm(forms.Form):

    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))

class LoginForm(ResetForm):

    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Your Password'}))

class SignupOneForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))
    full_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First and last name'}))

class SubscribeForm(LoginForm):
    full_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First and last name'}))
    company = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Company name'}))
    website = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Link to company website'}))
    soc_one = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Link to company Twitter'}), required=False,)
    soc_two = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Link to company Facebook'}), required=False,)
    soc_three = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Link to company LinkedIn'}), required=False,)
    soc_four = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Link to company Instagram'}), required=False,)

    Dev_Choices = (
        ('startup', 'Startup'),
        ('growth', 'Growth'),
        ('mature', 'Mature'),
    )
    dev_stage = forms.ChoiceField(choices=Dev_Choices)

    Sales_Choices = (
        ('less than $100k', 'Less than $100k'),
        ('less than $1 million', 'Less than $1 million'),
        ('over $1 milliion', 'Over $1 milliion'),
        ('over $10 milliion', 'Over $10 milliion'),
    )
    sales = forms.ChoiceField(choices=Sales_Choices)
    #industry = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Your industry'}))
    pitch = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'What is your mission statement and sales pitch? (pretend we are a customer of yours)', 'rows': 6}))
    industry = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Describe the industry you operate in. List some topics relevant to your industry and business.', 'rows': 4}))
    target_description = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Define your target market and buyer personas:\n - Where do they live?\n - What are their interests?\n - Social networks you know they are on?\n - Events that are popular for them?\n - Influencers they follow?', 'rows': 6}))
    brand_description = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Please briefly describe your brand as you see it and as want it to be.', 'rows': 4}))
    clients = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'List two current and two prospective clients/customers.'}))
    competition = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'List a couple of your primary competitors.'}))
    other = forms.CharField(required=False, min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Anything else you would like us to know? (optional)', 'rows': 2}))
    

    Goals_Choices = (
        ('brand awareness through followers', 'Increase brand awareness by increasing followers'),
        ('brand awareness through engagement', 'Increase brand awareness through community engagement'),
        ('sales leads', 'Generate sales leads'),
        ('drive traffic', 'Drive traffic to website'),
    )
    goals = forms.ChoiceField(choices=Goals_Choices)
    budget = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'What is your estimated monthly social media engagement spend?'}))
    creatives = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Will you be providing us your own marketing content regularly?\nIf so, how frequently?\nDescribe content you will provide us.\n(Images, White Papers, Press Releases, Blogs, etc.)', 'rows': 4}))

    #wants_ads = forms.BooleanField(required=False, label="I want to run display and text ads")
    #wants_social = forms.BooleanField(required=False, label="I want you to run my social media presence")
    wants_creatives = forms.BooleanField(required=False, label="I need you to build all creative content and/or social media profiles")

    promo = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Promo Code'}))

    Ads_Choices = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    #ads_scale = forms.ChoiceField(choices=Ads_Choices)

    Social_Choices = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    #social_scale = forms.ChoiceField(choices=Social_Choices)

class ReferralForm(forms.Form):
    ref = forms.CharField(min_length=8, max_length=8)

class DashboardForm(forms.Form):

    facebook_profile = forms.BooleanField(required=False)
    twitter_profile = forms.BooleanField(required=False)
    instagram_profile = forms.BooleanField(required=False)
    linkedin_profile = forms.BooleanField(required=False)
    marketing_strategy = forms.BooleanField(required=False)

    scale_choices = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    facebook_scale = forms.ChoiceField(required=False, choices=scale_choices)
    twitter_scale = forms.ChoiceField(required=False, choices=scale_choices)
    instagram_scale = forms.ChoiceField(required=False, choices=scale_choices)

    facebook_url = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Facebook Page URL'}))
    twitter_handle = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Twitter Handle'}))
    twitter_password = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Twitter Password'}))
    instagram_username = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Instagram Username'}))
    instagram_password = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Instagram Password'}))

class ActivateForm(forms.Form):
    
    id = forms.IntegerField(min_value=1000000, max_value=10000000)
    ref = forms.CharField(min_length=8, max_length=8)

class UpdateAdminForm(forms.Form):
    
    ref = forms.CharField(min_length=8, max_length=8)
    #goal = forms.CharField(required=False)
    #strategy = forms.CharField(required=False, widget=TinyMCE(attrs={'cols': 40, 'rows': 20}))
    active = forms.BooleanField(required=False)
    blocks_enabled = forms.BooleanField(required=False)
    hidden = forms.BooleanField(required=False)

class CompDescForm(forms.Form):
    storage = forms.CharField(required=False)
    goal = forms.CharField(required=False)
    strategy = forms.CharField(required=False, widget=TinyMCE(attrs={'cols': 40, 'rows': 40}))

