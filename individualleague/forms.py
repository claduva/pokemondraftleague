from django import forms
from django.contrib.auth.models import User

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
        c.append(('Playoff','Playoff'))
        self.fields['week']=forms.ChoiceField(choices=c)