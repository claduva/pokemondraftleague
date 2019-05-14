from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import *
from individualleague.models import schedule

class MatchReplayForm(forms.Form):
    url=forms.CharField(max_length=200,label="Replay URL")

class LeagueReplayForm(forms.ModelForm):
   
   class Meta:
        model = schedule
        fields = ['replay']