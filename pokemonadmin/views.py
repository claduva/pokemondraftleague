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

from datetime import datetime, timezone, timedelta
import pytz
import math

from .forms import *
from .models import *
from leagues.models import league_team
from pokemondatabase.models import *
from individualleague.models import *
from accounts.models import *

# Create your views here.
def pokemonadminhome(request):
    allroster=roster.objects.all().order_by('season','id')
    allmatch=schedule.objects.all().order_by('season','id')
    context={
        'adminsettings': True,
        'allroster':allroster,
        'allmatch':allmatch
    }
    if request.method=="POST":
        if request.POST['purpose']=="updatepokemon":
            pokemon=all_pokemon.objects.get(pokemon=request.POST['pokemontoupdate'])
            heading=f"Update {pokemon.pokemon}"
            form=UpdatePokemonForm(instance=pokemon)
            context.update({
                'heading':heading,
                'form':form,
                'formvalue':'updatepokemonsubmit',
                'pokemoninform':pokemon.pokemon,
            })
        elif request.POST['purpose']=="updatepokemonsubmit":
            pokemon=all_pokemon.objects.get(pokemon=request.POST['pokemontoupdate'])
            form=UpdatePokemonForm(request.POST,instance=pokemon)
            if form.is_valid():
                form.save()
                messages.success(request,f'Pokemon has been updated')
        elif request.POST['purpose']=="updateroster":
            rostertoupdate=roster.objects.get(id=request.POST['rostertoupdate'])
            heading=f"Update Roster"
            form=UpdateRosterForm(instance=rostertoupdate)
            context.update({
                'heading':heading,
                'form':form,
                'formvalue':'updaterostersubmit',
                'rosterinform':rostertoupdate.id,
            })
        elif request.POST['purpose']=="updaterostersubmit":
            rostertoupdate=roster.objects.get(id=request.POST['rostertoupdate'])
            form=UpdateRosterForm(request.POST,instance=rostertoupdate)
            if form.is_valid():
                form.save()
                messages.success(request,f'Roster has been updated')
        elif request.POST['purpose']=="updatematch":
            matchtoupdate=schedule.objects.get(id=request.POST['matchtoupdate'])
            heading=f"Update Match"
            form=UpdateMatchForm(instance=matchtoupdate)
            context.update({
                'heading':heading,
                'form':form,
                'formvalue':'updatematchsubmit',
                'matchinform':matchtoupdate.id,
            })
        elif request.POST['purpose']=="updatematchsubmit":
            matchtoupdate=schedule.objects.get(id=request.POST['matchtoupdate'])
            form=UpdateMatchForm(request.POST,instance=matchtoupdate)
            if form.is_valid():
                form.save()
                messages.success(request,f'Match has been updated')
        elif request.POST['purpose']=="sendsitemessage":
            heading=f"Send Site Message"
            form=SiteMessageForm()
            context.update({
                'heading':heading,
                'form':form,
                'formvalue':'sendmessagetoall',
            })
        elif request.POST['purpose']=="sendmessagetoall":
            form=SiteMessageForm(request.POST)
            if form.is_valid():
                messagesubject=form.cleaned_data['messagesubject']
                messagebody=form.cleaned_data['messagebody']
                admin=User.objects.get(username="Professor_Oak")
                allusers=User.objects.all().exclude(username=admin.username)
                for u in allusers:
                    inbox.objects.create(
                        sender=admin,
                        recipient=u,
                        messagesubject=messagesubject,
                        messagebody=messagebody
                    )
                messages.success(request,f'Message Sent')
    return  render(request,"adminsettings.html",context)