from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import *

class MatchReplayForm(forms.Form):
    url=forms.CharField(max_length=200,label="Replay URL")

