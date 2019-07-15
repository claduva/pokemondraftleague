from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput

from dal import autocomplete

from leagues.models import *
from .models import *

class CreateMatchForm(forms.ModelForm):
    
    class Meta:
        model = schedule
        fields = ['season','week','team1','team2']
        widgets = {'season': forms.HiddenInput()}

    def __init__(self,season,league, *args, **kwargs):
        super(CreateMatchForm, self).__init__(*args, **kwargs)
        self.fields['team1'].queryset = coachdata.objects.filter(league_name=league).order_by('teamname')
        self.fields['team1'].label_from_instance = lambda obj: obj.teamname
        self.fields['team2'].queryset = coachdata.objects.filter(league_name=league).order_by('teamname')
        self.fields['team2'].label_from_instance = lambda obj: obj.teamname
        c=[(i+1,i+1) for i in range(season.seasonlength)]
        d=[(f'Playoffs Round {i+1}',f'Playoffs Round {i+1}') for i in range(season.playoffslength-3)]
        e=[('Playoffs Quarterfinals','Playoffs Quarterfinals'),('Playoffs Semifinals','Playoffs Semifinals'),('Playoffs Third Place Match','Playoffs Third Place Match'),('Playoffs Finals','Playoffs Finals')]
        c=c+d+e
        self.fields['week']=forms.ChoiceField(choices=c)

class FreeAgencyForm(forms.ModelForm):
    
    class Meta:
        model = free_agency
        exclude = ['executed']
        widgets = {'season': forms.HiddenInput(),'coach':forms.HiddenInput(),'weekeffective':forms.HiddenInput()}

    def __init__(self,coachroster,availablepokemon, *args, **kwargs):
        super(FreeAgencyForm, self).__init__(*args, **kwargs)
        self.fields['droppedpokemon'].queryset = coachroster
        self.fields['droppedpokemon'].label_from_instance = lambda obj: obj.pokemon
        self.fields['addedpokemon'].queryset = availablepokemon

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
        self.fields['hall_of_frame_entry'].label_from_instance = lambda obj: obj.league.name + " " +obj.seasonname
       
class LeavePickForm(forms.ModelForm):
    
    class Meta:
        model = left_pick
        exclude = []
        widgets = {'season': forms.HiddenInput(),'coach':forms.HiddenInput(),}
        labels = {'pick': 'Pick','backup':'Backup',}
    
    def __init__(self,availablepokemon, *args, **kwargs):
        super(LeavePickForm, self).__init__(*args, **kwargs)
        self.fields['pick'].queryset = availablepokemon.order_by('pokemon')
        self.fields['backup'].queryset = availablepokemon.order_by('pokemon')

class ChangeMatchAttributionForm(forms.ModelForm):
    
    class Meta:
        model = schedule
        fields = ['team1','team1alternateattribution','team2','team2alternateattribution']

    def __init__(self, *args, **kwargs):
        super(ChangeMatchAttributionForm, self).__init__(*args, **kwargs)
        self.fields['team1alternateattribution'].required=False
        self.fields['team1alternateattribution'].queryset=User.objects.all().order_by('username')
        self.fields['team2alternateattribution'].required=False
        self.fields['team2alternateattribution'].queryset=User.objects.all().order_by('username')
        