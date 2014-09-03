from django import forms
from django.forms import widgets

class SubscribeForm(forms.Form):
    Age_Choices = (
        ('', ''),
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45+', '45+'),
    )
    age = forms.ChoiceField(choices=Age_Choices, required=False, label='Example')

    Style_Choices = (
        ('', ''),
        ('traditional', 'Traditional'),
        ('athletic', 'Athletic'),
        ('fashionista', 'Fashionista'),
        ('hip', 'Hip'),
        ('bookish', 'Bookish'),
    )
    style = forms.ChoiceField(choices=Style_Choices, required=False, label='Example')
    soc_one = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Social media link - Facebook, Pinterest, etc.'}), required=False,)
    soc_two = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Social media link - Facebook, Pinterest, etc.'}), required=False,)
    
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your Password'}))

class ContactForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your Email Address'}))
	message = forms.CharField(min_length=2, widget=forms.Textarea(attrs={'placeholder': 'Let us know right here...', 'rows': 4}))

class ReferralForm(forms.Form):
    ref = forms.CharField(min_length=8, max_length=8)
