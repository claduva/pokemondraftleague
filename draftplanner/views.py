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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse

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

@csrf_exempt
def getmon(request):
    lookupmon=request.POST['lookupmon']
    pokemonsearchlist=all_pokemon.objects.filter(pokemon__istartswith=lookupmon).order_by('pokemon')
    data=serializers.serialize('json', list(pokemonsearchlist),fields=('pokemon'))
    return HttpResponse(data, content_type='application/json')