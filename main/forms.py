from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import FileInput, CheckboxSelectMultiple, SelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import *
from accounts.models import inbox
from individualleague.models import *
from django.forms import DateTimeInput

class HelpForm(forms.ModelForm):

    messagesubject=forms.CharField(max_length=100,label='Subject')

    class Meta:
        model = inbox
        exclude = ['read']
        widgets = {
            'sender': forms.HiddenInput(),
            'recipient': forms.HiddenInput(),
            }
        labels = {
            'messagebody': 'Message',
            }
