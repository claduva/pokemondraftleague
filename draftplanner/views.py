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
from django.forms.models import model_to_dict

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

@login_required
def draftplanner(request):
    usersdrafts=planned_draft.objects.all().filter(user=request.user)
    defaultname=None
    i=1
    try:
        planned_draft.objects.all().filter(user=request.user).get(draftname="Untitled")
        while defaultname == None:
            try:
                planned_draft.objects.all().filter(user=request.user).get(draftname=f"Untitled{i}")
            except:
                defaultname= f"Untitled{i}"
            i+=1
    except:
        defaultname="Untitled"
    pokemondatabase=list(all_pokemon.objects.all().values_list('data',flat=True))
    pokemonlist=list(all_pokemon.objects.all().values_list('pokemon',flat=True))
    typelist=list(pokemon_type.objects.all().order_by('typing').distinct('typing').values_list('typing',flat=True))
    abilitylist=list(pokemon_ability.objects.all().order_by('ability').distinct('ability').values_list('ability',flat=True))
    movelist=list(moveinfo.objects.all().order_by('name').distinct('name').values_list('name',flat=True))
    try:  
        site_settings = request.user.sitesettings
    except:
        user=User.objects.get(username="defaultuser")
        site_settings = user.sitesettings
    context = {
        'usersdrafts':usersdrafts,
        'defaultname':defaultname,
        'pokemondatabase':pokemondatabase,
        'pokemonlist':pokemonlist,
        'typelist':typelist,
        'movelist':movelist,
        'abilitylist':abilitylist,
        'spriteurl': str(site_settings.sprite),
    }
    return render(request, 'draftplanner.html',context)

@csrf_exempt
def getdraft(request):
    lookupdraft=request.POST['lookupdraft']
    lookupdraft=planned_draft.objects.get(id=lookupdraft)
    pokemonlist=[]
    for item in lookupdraft.pokemonlist.all():
        pokemonlist.append(item.pokemon)
    if lookupdraft.associatedleague:
        associatedleague=lookupdraft.associatedleague.id
    else:
        associatedleague="None"
    data={
        'draftname':lookupdraft.draftname,
        'associatedleague':associatedleague,
        'lookupdraft': pokemonlist,
        'draftloaded':lookupdraft.id,
        }
    return JsonResponse(data)

@csrf_exempt
def savedraft(request):
    drafttoeditid=''
    draftname=request.POST['draftname']
    associatedleague=request.POST['associatedleague']
    if associatedleague != 'None':
        associatedleague=league.objects.get(id=associatedleague)
    else:
        associatedleague=None
    savelist=request.POST.getlist('savelist[]')
    existingdraft=request.POST['existingdraft']
    if len(savelist)>0:
        if existingdraft=='':
            drafttoedit=planned_draft.objects.create(
                id=planned_draft.objects.all().order_by('-id').first().id+1,
                user = request.user,
                associatedleague = associatedleague,
                draftname = draftname
            )
            for item in savelist:
                pokemontoadd=all_pokemon.objects.get(pokemon=item)
                drafttoedit.pokemonlist.add(pokemontoadd)
            drafttoedit.save()
        else:
            drafttoedit=planned_draft.objects.get(id=int(existingdraft))
            drafttoedit.draftname=draftname
            drafttoedit.associatedleague=associatedleague
            drafttoedit.pokemonlist.clear()
            for item in savelist:
                pokemontoadd=all_pokemon.objects.get(pokemon=item)
                drafttoedit.pokemonlist.add(pokemontoadd)
            drafttoedit.save()
        drafttoeditid=drafttoedit.id
    data={'response':drafttoeditid}
    return JsonResponse(data)

@csrf_exempt
def deletedraft(request):
    loadeddraft=request.POST['loadeddraft']
    try:
        planned_draft.objects.get(id=int(loadeddraft)).delete()
        response="Success"
    except:
        response="Fail"
    data={
        'response':response
        }
    return JsonResponse(data)