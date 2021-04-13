from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from django.contrib.admin.widgets import FilteredSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from dal import autocomplete

from leagues.models import *
from .models import *

class FreeAgencyForm(forms.ModelForm):
    
    class Meta:
        model = free_agency
        exclude = ['executed']
        widgets = {'season': forms.HiddenInput(),'coach':forms.HiddenInput(),'weekeffective':forms.HiddenInput()}

    def __init__(self,droppedpokemon,availablepokemon, *args, **kwargs):
        super(FreeAgencyForm, self).__init__(*args, **kwargs)
        self.fields['droppedpokemon'].queryset = all_pokemon.objects.all().filter(id__in=droppedpokemon.values_list('pokemon',flat=True))
        self.fields['addedpokemon'].queryset = all_pokemon.objects.all().filter(id__in=availablepokemon.values_list('pokemon',flat=True))

class TradeRequestForm(forms.ModelForm):
    
    class Meta:
        model = trade_request
        exclude = []

    def __init__(self,coachroster,availablepokemon, *args, **kwargs):
        super(TradeRequestForm, self).__init__(*args, **kwargs)
        self.fields['offeredpokemon'].queryset = coachroster
        self.fields['offeredpokemon'].label_from_instance = lambda obj: obj.pokemon.pokemon
        self.fields['requestedpokemon'].queryset = availablepokemon
        self.fields['requestedpokemon'].label_from_instance = lambda obj: obj.pokemon.pokemon + " ("+obj.team.teamname+")"

class RuleChangeForm(forms.ModelForm):
    
    class Meta:
        model = rule
        exclude = ['season']


class AddHallOfFameEntryForm(forms.ModelForm):
    champlogo=forms.FileField(widget=FileInput)
    
    class Meta:
        model = hall_of_fame_entry
        exclude = []
        widgets = {'league': forms.HiddenInput()}

class AddHallOfFameRosterForm(forms.ModelForm):
    
    class Meta:
        model = hall_of_fame_roster
        exclude = []
        widgets = {
            'pokemon': autocomplete.ModelSelect2(url='pokemon-autocomplete')
        }
       

    def __init__(self, *args, **kwargs):
        super(AddHallOfFameRosterForm, self).__init__(*args, **kwargs)
        self.fields['pokemon'].queryset = all_pokemon.objects.all().order_by('pokemon')
        self.fields['hall_of_frame_entry'].label_from_instance = lambda obj: f'{obj.league.name}'
       
class LeavePickForm(forms.ModelForm):
    
    class Meta:
        model = left_pick
        exclude = []
        widgets = {
            'season': forms.HiddenInput(),'coach':forms.HiddenInput(),
            'pick':autocomplete.ModelSelect2(url='pokemon-autocomplete'),
            'backup':autocomplete.ModelSelect2(url='pokemon-autocomplete'),
            }
        labels = {'pick': 'Pick','backup':'Backup',}
    
    def __init__(self,availablepokemon, *args, **kwargs):
        super(LeavePickForm, self).__init__(*args, **kwargs)
        self.fields['pick'].queryset = availablepokemon.order_by('pokemon')
        self.fields['backup'].queryset = availablepokemon.order_by('pokemon')

class ChangeMatchAttributionForm(forms.ModelForm):
    
    class Meta:
        model = schedule
        fields = ['team1','team1alternateattribution','team2','team2alternateattribution','team1score','team2score','winner','winneralternateattribution']

    def __init__(self, *args, **kwargs):
        super(ChangeMatchAttributionForm, self).__init__(*args, **kwargs)
        self.fields['team1alternateattribution'].required=False
        self.fields['team1alternateattribution'].queryset=User.objects.all().order_by('username')
        self.fields['team2alternateattribution'].required=False
        self.fields['team2alternateattribution'].queryset=User.objects.all().order_by('username')
        self.fields['winner'].required=False
        self.fields['winneralternateattribution'].required=False
        self.fields['winneralternateattribution'].queryset=User.objects.all().order_by('username')
        
class LeagueApplicationForm(forms.ModelForm):
    
    class Meta:
        model = league_application
        fields = ['applicant','league_name','discord_name','teamabbreviation','teamname','draft_league_resume','tier_preference','willingtobealternate']
        
        widgets = {
            'applicant': forms.HiddenInput(),
            'league_name': forms.HiddenInput(),
            'tier_preference': forms.CheckboxSelectMultiple()
            }
    
    def __init__(self,league, *args, **kwargs):
        super(LeagueApplicationForm, self).__init__(*args, **kwargs)
        #self.fields["tier_preference"].widget = FilteredSelectMultiple("league_subleague", False, attrs={'rows':'2'})
        self.fields["tier_preference"].queryset = league_subleague.objects.all().filter(league=league)
        self.fields["willingtobealternate"].label="Check If Willing to Serve as Alternate"
        self.fields["teamabbreviation"].label="Team Abbreviation"
        self.fields["teamname"].label="Team Name"
        self.fields["discord_name"].label="Discord Username"
        self.fields["tier_preference"].label="Which subleagues are you interested in? (Select All That Apply)"

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Apply'))
        self.helper.layout = Layout(
            Row(
                Column('applicant', css_class='form-group col-md-6 mb-0'),
                Column('league_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(
                Column('discord_name', css_class='form-group col-md-3 mb-0'),
                Column('teamabbreviation', css_class='form-group col-md-3 mb-0'),
                Column('teamname', css_class='form-group col-md-4 mb-0'),
                Column('willingtobealternate', css_class='form-group col-md-2 mb-0'),
                css_class='form-row align-items-center'),
            Row(
                Column('draft_league_resume', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'),
            Row(
                Column('tier_preference', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'),
        )