from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import *

from pokemondatabase.models import *
from leagues.models import *
from individualleague.models import *
from accounts.models import *

class UpdatePokemonForm(forms.ModelForm):

    class Meta:
        model = all_pokemon
        fields = ['kills','deaths','differential','gp','gw','timesdrafted']

class UpdateRosterForm(forms.ModelForm):

    class Meta:
        model = roster
        fields = ['pokemon','kills','deaths','differential','gp','gw','zuser']

class UpdateMatchForm(forms.ModelForm):

    class Meta:
        model = schedule
        exclude = ['season']

class SiteMessageForm(forms.ModelForm):

    class Meta:
        model = inbox
        fields = ['messagesubject','messagebody']

class ChangeHistoricMatchAttributionForm(forms.ModelForm):
    
    class Meta:
        model = historical_match
        fields = ['team1','team1alternateattribution','team2','team2alternateattribution','team1score','team2score','winner','winneralternateattribution']

    def __init__(self, *args, **kwargs):
        super(ChangeHistoricMatchAttributionForm, self).__init__(*args, **kwargs)
        self.fields['team1alternateattribution'].required=False
        self.fields['team1alternateattribution'].queryset=User.objects.all().order_by('username')
        self.fields['team2alternateattribution'].required=False
        self.fields['team2alternateattribution'].queryset=User.objects.all().order_by('username')
        self.fields['winner'].required=False
        self.fields['winneralternateattribution'].required=False
        self.fields['winneralternateattribution'].queryset=User.objects.all().order_by('username')