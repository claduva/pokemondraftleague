from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput

from dal import autocomplete

from leagues.models import *
from .models import *
from individualleague.models import *

class Pokedex(forms.ModelForm):
    
    class Meta:
        model = hall_of_fame_roster
        fields = ['pokemon']
        widgets = {
            'pokemon': autocomplete.ModelSelect2(url='pokemon-autocomplete')
        }
        labels = {
            'pokemon': 'Choose A Pokemon'
        }

    def __init__(self, *args, **kwargs):
        super(Pokedex, self).__init__(*args, **kwargs)
        self.fields['pokemon'].queryset = all_pokemon.objects.all().order_by('pokemon')       