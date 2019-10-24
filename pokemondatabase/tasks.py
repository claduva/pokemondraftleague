from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import math
from django.db.models import Q
from django.contrib.auth.models import User

from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *
from .models import *

from pokemondraftleague.celery import app

@shared_task(name = "pokemon_stat_update")
def pokemon_stat_update():
    leaderboard=pokemon_leaderboard.objects.all()
    for item in leaderboard:
        #set baseline
        item.kills=item.pokemon.kills
        item.deaths=item.pokemon.deaths
        item.differential = item.pokemon.differential
        item.gp=item.pokemon.gp
        item.gw=item.pokemon.gw
        item.timesdrafted=0 
        item.support=item.pokemon.support
        item.damagedone=item.pokemon.damagedone
        item.hphealed=item.pokemon.hphealed
        item.luck =item.pokemon.luck
        item.remaininghealth=item.pokemon.remaininghealth
        item.save()
        #update based on rosters
        rosterson=item.pokemon.pokemonroster.all()
        for team in rosterson:
            if team.season.league.name.find('Test')==-1:
                item.kills+=team.kills
                item.deaths+=team.deaths
                item.differential+=team.differential
                item.gp+=team.gp
                item.gw+=team.gw
                item.support=team.support
                item.damagedone=team.damagedone
                item.hphealed=team.hphealed
                item.luck=team.luck
                item.remaininghealth=team.remaininghealth
        historicrosterson=item.pokemon.historicalpokemonroster.all()
        for team in historicrosterson:
            if team.team.league.name.find('Test')==-1:
                item.kills+=team.kills
                item.deaths+=team.deaths
                item.differential+=team.differential
                item.gp+=team.gp
                item.gw+=team.gw
                item.support=team.support
                item.damagedone=team.damagedone
                item.hphealed=team.hphealed
                item.luck=team.luck
                item.remaininghealth=team.remaininghealth
        item.timesdrafted=item.pokemon.historicalpokemondraft.all().count()+item.pokemon.pokemondraft.all().count()
        item.save()