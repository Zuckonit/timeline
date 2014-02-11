from django import forms 
from django.contrib.admin import widgets
from models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=16, min_length=3)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=16, min_length=3, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6, required=True)
    re_password = forms.CharField(label='Repeat', widget=forms.PasswordInput(), min_length=6)
    email = forms.EmailField(label='email')

class ProfileForm(forms.Form):
    SEX_CHOICE = [(2, ''), (0, 'female'), (1, 'male')]
    sex = forms.ChoiceField(choices=SEX_CHOICE, widget=forms.RadioSelect())
    birthday = forms.ChoiceField(widget=widgets.AdminDateWidget())
    
