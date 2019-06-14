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
from datetime import datetime
import time

from accounts.forms import UserRegisterForm
from .models import *
from leagues.models import *

# Create your views here.
def pokedex(request):
    if request.method=='POST':
        pokemon_of_interest=request.POST['pokemonpick']
        return redirect('pokedex_item',pokemon_of_interest=pokemon_of_interest)
    context = {
        "title": 'Pokemon Info',
        "pokedex": True,
    }
    return render(request,"pokedex.html", context)

def pokedex_item(request,pokemon_of_interest):
    try:
        pokemon_data=all_pokemon.objects.get(pokemon=pokemon_of_interest)
        draftnumber=draft.objects.all().filter(pokemon=pokemon_data).count()
        pokemon_data.timesdrafted+=draftnumber
        roster_data=roster.objects.all().filter(pokemon=pokemon_data)
        print(roster_data)
        for item in roster_data:
            pokemon_data.kills+=item.kills
            pokemon_data.deaths+=item.deaths
            pokemon_data.differential+=item.differential
            pokemon_data.gp+=item.gp
            pokemon_data.gw+=item.gw
    except:
        messages.error(request,'Pokemon does not exist!',extra_tags='danger')
        return redirect('pokedex')
    context = {
        "title": pokemon_of_interest,
        'pokedexitem': True,
        'pokemon_data':pokemon_data,
    }
    return render(request,"pokedex.html", context)

