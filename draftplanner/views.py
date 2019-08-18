from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

import json
import math
from datetime import datetime, timezone, timedelta
import pytz

from dal import autocomplete

from .models import *
from leagues.models import *
from pokemondatabase.models import *
from accounts.models import *
from datetime import datetime, timedelta,timezone
from operator import itemgetter

def draftplanner(request):
    context = {
    }
    return render(request, 'draftplanner.html',context)