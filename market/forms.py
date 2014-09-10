from django import forms
from django.forms import widgets

class LoginForm(forms.Form):

    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Your Password'}))

class SubscribeForm(LoginForm):
    
    company = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Company name'}))
    website = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Company website'}))
    soc_one = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'URL to social media profile (optional)'}), required=False,)
    soc_two = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'URL to social media profile (optional)'}), required=False,)
    soc_three = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'URL to social media profile (optional)'}), required=False,)

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
    industry = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Your industry'}))
    co_description = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Please briefly describe your business and target audience (if known).', 'rows': 4}))
    brand_description = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Please briefly describe your brand as you see it and as want it to be.', 'rows': 4}))
    competition = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'List your primary competition.'}))
    other = forms.CharField(required=False, min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Anything else you would like us to know? (optional)', 'rows': 2}))
    
    Goals_Choices = (
        ('brand awareness', 'Brand awareness'),
        ('engagement', 'Engagement'),
        ('driving sales', 'Driving Sales'),
    )
    goals = forms.ChoiceField(choices=Goals_Choices)
    wants_ads = forms.BooleanField(required=False, label="I want to run display and text ads")
    wants_social = forms.BooleanField(required=False, label="I want you to run my social media presence")
    wants_creatives = forms.BooleanField(required=False, label="I need you to design ad creatives and/or build my social media profiles")

class ReferralForm(forms.Form):
    ref = forms.CharField(min_length=8, max_length=8)
