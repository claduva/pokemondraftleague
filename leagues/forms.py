from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import *

class CreateLeagueForm(forms.ModelForm):

    class Meta:
        model = league
        fields = ['name','host']
        widgets = {'host': forms.HiddenInput()}

class UpdateLeagueForm(forms.ModelForm):
    logo=forms.FileField(widget=FileInput)
    
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
    logo=forms.FileField(widget=FileInput)

    class Meta:
        model = coachdata
        fields = ['logo','teamabbreviation','teamname']

class UpdateCoachTeammateForm(forms.ModelForm):
    teammate = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = coachdata
        fields = ['teammate']

class CreateSeasonSettingsForm(forms.ModelForm):

    class Meta:
        model = seasonsetting
        fields = ['league','seasonname','draftbudget','drafttype','picksperteam','seasonlength','freeagenciesallowed','tradesallowed','numzusers','candeletez']
        widgets = {
            'league': forms.HiddenInput(),
            }

class EditSeasonSettingsForm(forms.ModelForm):

    class Meta:
        model = seasonsetting
        fields = ['seasonname','draftbudget','drafttype','seasonlength','freeagenciesallowed','tradesallowed','numzusers','candeletez']

class ManageCoachForm(forms.ModelForm):
    logo=forms.FileField(widget=FileInput,required=False)

    class Meta:
        model = coachdata
        fields = ['teamname','teamabbreviation','logo','teammate','conference','division']

    def __init__(self,league, *args, **kwargs):
        super(ManageCoachForm, self).__init__(*args, **kwargs)
        self.fields['conference'].queryset = conference_name.objects.filter(league=league).order_by('name')
        self.fields['division'].queryset = division_name.objects.filter(league=league).order_by('name')
        self.fields['division'].required = False
        self.fields['teammate'].required=False

class DesignateZUserForm(forms.Form):
    zuser = forms.ModelChoiceField(queryset=roster.objects.all(), required=True)
    zmovetype = forms.ChoiceField(choices=(
        ("OS","Offensive & Status"),
        ("O","Offensive"),
    ))
    class Meta:
        fields = ['zuser','zmovetype']
    
    def __init__(self,season,team,*args, **kwargs):
        super(DesignateZUserForm, self).__init__(*args, **kwargs)
        self.fields['zuser'].queryset = roster.objects.all().filter(season=season,team=team).order_by('pokemon__pokemon')
        self.fields['zuser'].label_from_instance = lambda obj: obj.pokemon.pokemon