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
