from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput

from dal import autocomplete

from leagues.models import *
from .models import *


