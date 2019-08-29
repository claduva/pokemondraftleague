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
    context = {
        'usersdrafts':usersdrafts,
        'defaultname':defaultname,
    }
    return render(request, 'draftplanner.html',context)

@csrf_exempt
def getmon(request):
    lookupmon=request.POST['lookupmon']
    pokemonsearchlist=all_pokemon.objects.filter(pokemon__istartswith=lookupmon).order_by('pokemon')
    data=serializers.serialize('json', list(pokemonsearchlist),fields=('pokemon'))
    return HttpResponse(data, content_type='application/json')

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
            if associatedleague != 'None':
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
    planned_draft.objects.get(id=int(loadeddraft)).delete()
    data={
        'response':'Success'
        }
    return JsonResponse(data)

@csrf_exempt
def updatedata(request):
    savelist=request.POST.getlist('savelist[]')
    data=[]
    speeds=[]
    for item in savelist:
        monofinterest=all_pokemon.objects.get(pokemon=item)
        #moveset
        movesofinterest=["Stealth Rock","Spikes","Toxic Spikes","Sticky Web","Rapid Spin","Defog","Wish","Heal Bell","Aromatherapy"]
        for m in monofinterest.moves.all().filter(moveinfo__name__in=movesofinterest):
            if m.moveinfo.name=="Aromatherapy" or m.moveinfo.name=="Heal Bell":
                data.append((f"#Cleric",item,'Y'))
            elif m.moveinfo.name.find(" ")>-1:
                data.append((f"#{m.moveinfo.name.replace(' ','')}",item,'Y'))
            else:
                data.append((f"#{m.moveinfo.name}",item,'Y'))
        #types
        for t in monofinterest.types.all():
            data.append((f"#{t.typing}",item,'Y'))
        #monspeed
        monspeed=monofinterest.speed
        speeds.append(monspeed)
        if monspeed<31:
            data.append(("#speed_g1",item,'Y'))
        elif monspeed<51:
            data.append(("#speed_g2",item,'Y'))
        elif monspeed<71:
            data.append(("#speed_g3",item,'Y'))
        elif monspeed<91:
            data.append(("#speed_g4",item,'Y'))
        elif monspeed<111:
            data.append(("#speed_g5",item,'Y'))
        elif monspeed >110:
            data.append(("#speed_g6",item,'Y'))
    #max speed gap
    if len(speeds)>1:
        speeds.sort()
        maxdif=0
        for i in range(len(speeds)-1):
            dif=speeds[i+1]-speeds[i]
            if dif>maxdif:
                maxdif=dif
        data.append(("#largestspeedgap",maxdif,'N'))
    data={
        'response': data
        }
    return JsonResponse(data)