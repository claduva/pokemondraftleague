from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    pfp=forms.FileField(widget=FileInput,required=False)
    class Meta:
        model = profile
        fields = ['pfp','discordid']
        labels = {
        "pfp": "Profile Picture"
        
    }

class SiteSettingUpdateForm(forms.ModelForm):
    class Meta:
        model = sitesettings
        fields = ['sprite']

class ShowdowAltAddForm(forms.ModelForm):
    
    class Meta:
        model = showdownalts
        fields = ['showdownalt']
        widgets = {'user': forms.HiddenInput()}
