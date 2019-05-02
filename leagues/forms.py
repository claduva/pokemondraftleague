from django import forms
from django.contrib.auth.models import User
from .models import *

class CreateLeagueForm(forms.ModelForm):

    class Meta:
        model = league
        fields = ['name','host']
        widgets = {'host': forms.HiddenInput()}

class UpdateLeagueForm(forms.ModelForm):

    class Meta:
        model = league
        fields = ['name','host','logo']

class UpdateLeagueSettingsForm(forms.ModelForm):

    class Meta:
        model = league_settings
        fields = ['is_recruiting','discordurl','number_of_teams','number_of_conferences','number_of_divisions']

class LeagueApplicationForm(forms.ModelForm):
    
    class Meta:
        model = league_application
        fields = ['applicant','league_name']
        widgets = {
            'applicant': forms.HiddenInput(),
            'league_name': forms.HiddenInput(),
            }