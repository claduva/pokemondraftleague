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
        fields = ['is_recruiting','discordurl','number_of_teams','number_of_conferences','number_of_divisions','allows_teams']

class LeagueApplicationForm(forms.ModelForm):
    
    class Meta:
        model = league_application
        fields = ['applicant','league_name']
        widgets = {
            'applicant': forms.HiddenInput(),
            'league_name': forms.HiddenInput(),
            }

class CreateTierForm(forms.ModelForm):
    
    class Meta:
        model = leaguetiers
        fields = ['league','tiername','tierpoints']
        widgets = {
            'league': forms.HiddenInput(),
            }

class UpdateTierForm(forms.ModelForm):
    
    class Meta:
        model = leaguetiers
        fields = ['league','tiername','tierpoints']
        widgets = {
            'league': forms.HiddenInput(),
            }

class UpdateCoachInfoForm(forms.ModelForm):

    class Meta:
        model = coachdata
        fields = ['logo','teamabbreviation','teamname']

class UpdateCoachTeammateForm(forms.ModelForm):
    teammate = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = coachdata
        fields = ['teammate']