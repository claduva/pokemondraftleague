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

import math

from .models import *
from leagues.models import *
from pokemondatabase.models import *
from accounts.models import *
from .forms import *
from datetime import datetime, timedelta,timezone

def team_page(request,league_name,team_abbreviation):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        team=coachdata.objects.filter(league_name=league_,teamabbreviation=team_abbreviation).first()
        try:
            season=seasonsetting.objects.get(league=league_)
            teamroster=roster.objects.all().filter(season=season,team=team).order_by('id')
        except:
            teamroster=None   
    except:
        messages.error(request,'Team does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name) 
    league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    matchs=schedule.objects.all().filter(season=season).filter(Q(team1=team)|Q(team2=team))
    results=matchs.exclude(replay="Link").order_by('-id')
    upcoming=matchs.filter(replay="Link").order_by('id')[0:4]
    context = {
        'league': league_,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'team': team,
        'roster': teamroster,
        'results':results,
        'upcoming': upcoming
    }
    return render(request, 'teampage.html',context)

def league_draft(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
        draftstart=str(season.draftstart)
        drafttimer=season.drafttimer
        
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    try:
        draftlist=draft.objects.all().filter(season=season).order_by('id') 
        draftsize=draftlist.count()
        picksremaining=draftlist.filter(pokemon__isnull=True).count()
        draftprogress=int(math.floor((draftsize-picksremaining)/draftsize*100))
    except:
        messages.error(request,'Draft does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    is_host=(request.user==league_.host)
    currentpick=draftlist.filter(pokemon__isnull=True).first()
    if currentpick==None:
        draftactive=False
        availablepoints=0
    else:
        draftactive=True
        draftersroster=roster.objects.all().filter(season=season,team=currentpick.team)
        pointsused=0
        for item in draftersroster:
            tier=pokemon_tier.objects.filter(league=league_,pokemon=item.pokemon).first()
            if tier != None:    
                pointsused+=tier.tier.tierpoints
        budget=season.draftbudget
        availablepoints=budget-pointsused
    if picksremaining==draftsize:
        pickend=str(season.draftstart+timedelta(hours=12))
    else:    
        pickend=str(draftlist.get(id=currentpick.id-1).picktime+timedelta(hours=12))
    if request.method == "POST":
        try:
            draftpick=all_pokemon.objects.get(pokemon=request.POST['draftpick'])
        except:
            messages.error(request,f'{request.POST["draftpick"]} is not a pokemon!',extra_tags='danger')
            return redirect('league_draft',league_name=league_name)
        searchroster=roster.objects.filter(season=season,pokemon=draftpick).first()
        if searchroster!=None:
            messages.error(request,f'{draftpick.pokemon } has already been drafted!',extra_tags='danger')
            return redirect('league_draft',league_name=league_name)
        currentpick.pokemon=draftpick
        rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
        rosterspot.pokemon=draftpick
        currentpick.save()
        rosterspot.save()
        messages.success(request,'Your draft pick has been saved!')
        return redirect('league_draft',league_name=league_name)
    availablepokemon=all_pokemon.objects.all().order_by('pokemon')
    for item in availablepokemon:
        tiering=pokemon_tier.objects.all().filter(league=league_,pokemon=item).first()
        if tiering.tier.tiername=="Banned":
            availablepokemon=availablepokemon.all().exclude(pokemon=item)
        else:
            rosteritem=roster.objects.filter(season=season,pokemon=item).first()
            if rosteritem != None:
                availablepokemon=availablepokemon.all().exclude(pokemon=item)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'draftlist': draftlist,
        'draftstartid': -(draftlist.first().id-1),
        'currentpick':currentpick,
        'availablepokemon': availablepokemon,
        'draftactive': draftactive,
        'availablepoints':availablepoints,
        'draftprogress':draftprogress,
        'is_host': is_host,
        'draftstart': draftstart,
        'pickend':pickend,
    }
    return render(request, 'draft.html',context)

@login_required
def create_match(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != league_.host:
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    leaguesettings=league_settings.objects.get(league_name=league_)
    needednumberofcoaches=leaguesettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=league_)
    currentcoachescount=len(currentcoaches)
    try:
        seasonsettings=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if needednumberofcoaches != currentcoachescount: 
        messages.error(request,'You can only utilize season settings if you have designated the same number of coaches as available spots',extra_tags='danger')
        return redirect('individual_league_settings',league_name=league_name)
    if request.method == 'POST':   
        form = CreateMatchForm(seasonsettings,league_,request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'That match has been added!')
        return redirect('create_match',league_name=league_name)
    form = CreateMatchForm(seasonsettings,league_,initial={'season':seasonsettings})
    settingheading='Create New Match'
    create=True
    manageseason=False
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'league_teams': league_teams,
        'forms': [form],
        'seasonsettings': seasonsettings,
        'settingheading': settingheading,
        'create': create,
        'manageseason': manageseason,
    }
    return render(request, 'settings.html',context)

def league_schedule(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    leagueschedule=[]
    numberofweeks=season.seasonlength
    for i in range(numberofweeks):
        matches=schedule.objects.all().filter(week=str(i+1)).order_by('id')
        leagueschedule.append(matches)
    ishost=(request.user==league_.host)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'leagueschedule': leagueschedule,
        'ishost': ishost
    }
    return render(request, 'schedule.html',context)

def league_matchup(request,league_name,matchid):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    try:
        match=schedule.objects.get(id=matchid)
    except:
        messages.error(request,'Match does not exist!',extra_tags='danger')
        return redirect('league_schedule',league_name=league_name)
    team1roster_=roster.objects.filter(season=season,team=match.team1).order_by('pokemon__pokemon')
    team1roster=[]
    defog=[]
    rapidspin=[]
    sr=[]
    spikes=[]
    tspikes=[]
    stickyweb=[]
    healbell=[]
    wish=[]
    for item in team1roster_:
        typing=pokemon_type.objects.all().filter(pokemon=item.pokemon)
        abilities=pokemon_ability.objects.all().filter(pokemon=item.pokemon)
        basespeed=item.pokemon.speed
        base50=math.floor((((2*basespeed+31+252/4)*50)/100+5)*1.1)
        base100=math.floor((((2*basespeed+31+252/4)*100)/100+5)*1.1)
        speeds=[math.floor(base50*2/3),base50,math.floor(base50*3/2),math.floor(base50*2),math.floor(base100*2/3),base100,math.floor(base100*3/2),math.floor(base100*2)]
        team1roster.append([item,typing,abilities,speeds])
        moveset=pokemon_moveset.objects.all().filter(pokemon=item.pokemon)
        healaroma=True
        for move in moveset:
            if move.moveinfo.name=="Defog":
                defog.append(item)
            if move.moveinfo.name=="Rapid Spin":
                rapidspin.append(item)
            if move.moveinfo.name=="Stealth Rock":
                sr.append(item)
            if move.moveinfo.name=="Spikes":
                spikes.append(item)
            if move.moveinfo.name=="Toxic Spikes":
                tspikes.append(item)
            if move.moveinfo.name=="Sticky Web":
                stickyweb.append(item)
            if move.moveinfo.name=="Aromatherapy" and healaroma:
                healbell.append(item)
                healaroma=False
            if move.moveinfo.name=="Heal Bell" and healaroma:
                healbell.append(item)
                healaroma=False
            if move.moveinfo.name=="Wish":
                wish.append(item)
    team1moves=[['Stealth Rock',sr],['Spikes',spikes],['Toxic Spikes',tspikes],['Sticky Web',stickyweb],['Defog',defog],['Rapid Spin',rapidspin],['Heal Bell/Aromatherapy',healbell],['Wish',wish]]

    team2roster_=roster.objects.filter(season=season,team=match.team2).order_by('pokemon__pokemon')
    team2roster=[]
    defog=[]
    rapidspin=[]
    sr=[]
    spikes=[]
    tspikes=[]
    stickyweb=[]
    healbell=[]
    wish=[]
    for item in team2roster_:
        typing=pokemon_type.objects.all().filter(pokemon=item.pokemon)
        abilities=pokemon_ability.objects.all().filter(pokemon=item.pokemon)
        basespeed=item.pokemon.speed
        base50=math.floor((((2*basespeed+31+252/4)*50)/100+5)*1.1)
        base100=math.floor((((2*basespeed+31+252/4)*100)/100+5)*1.1)
        speeds=[math.floor(base50*2/3),base50,math.floor(base50*3/2),math.floor(base50*2),math.floor(base100*2/3),base100,math.floor(base100*3/2),math.floor(base100*2)]
        team2roster.append([item,typing,abilities,speeds])
        moveset=pokemon_moveset.objects.all().filter(pokemon=item.pokemon)
        healaroma=True
        for move in moveset:
            if move.moveinfo.name=="Defog":
                defog.append(item)
            if move.moveinfo.name=="Rapid Spin":
                rapidspin.append(item)
            if move.moveinfo.name=="Stealth Rock":
                sr.append(item)
            if move.moveinfo.name=="Spikes":
                spikes.append(item)
            if move.moveinfo.name=="Toxic Spikes":
                tspikes.append(item)
            if move.moveinfo.name=="Sticky Web":
                stickyweb.append(item)
            if move.moveinfo.name=="Aromatherapy" and healaroma:
                healbell.append(item)
                healaroma=False
            if move.moveinfo.name=="Heal Bell" and healaroma:
                healbell.append(item)
                healaroma=False
            if move.moveinfo.name=="Wish":
                wish.append(item)
    team2moves=[['Stealth Rock',sr],['Spikes',spikes],['Toxic Spikes',tspikes],['Sticky Web',stickyweb],['Defog',defog],['Rapid Spin',rapidspin],['Heal Bell/Aromatherapy',healbell],['Wish',wish]]

    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'match': match,
        'team1roster': team1roster,
        'team2roster': team2roster,
        'team1moves': team1moves,
        'team2moves': team2moves,
    }
    return render(request, 'matchup.html',context)


def league_rules(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    ruleset=rule.objects.get(season=season)
    is_host=(request.user==league_.host)
    edit=False
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'ruleset': ruleset,
        'is_host': is_host,
        'edit': edit,
    }
    return render(request, 'rules.html',context)

def league_tiers(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    tiers=leaguetiers.objects.all().filter(league=league_).order_by('-tierpoints')
    mega=[]
    tierlist=[]
    banned=False
    for item in tiers:
        tieritems=[]
        tieritems_=pokemon_tier.objects.all().filter(tier=item).order_by('pokemon__pokemon')
        for pokemon in tieritems_:
            try:    
                rosterspot=roster.objects.all().filter(season=season).get(pokemon=pokemon.pokemon)
                team=rosterspot.team
            except:
                team=None
            tieritems.append([pokemon,team])
        if item.tiername.find("Mega")>-1:
            mega.append([item,tieritems])   
        elif item.tiername.find("Banned")>-1:
            banned=True 
        else:
            tierlist.append([item,tieritems]) 
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'tiers': tierlist,
        'mega': mega,
        'banned': banned,
    }
    return render(request, 'tiers.html',context)

def individual_league_tier(request,league_name,tiername):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    try:
        tiername=tiername.replace("_"," ")
        tierofinterest=leaguetiers.objects.all().filter(league=league_).get(tiername=tiername)
        tiers=[]
        tiers_=pokemon_tier.objects.all().filter(tier=tierofinterest).order_by('pokemon__pokemon')
        for item in tiers_:
            try:    
                rosterspot=roster.objects.all().filter(season=season).get(pokemon=item.pokemon)
                team=rosterspot.team
            except:
                team=None
            tiers.append([item,team])
        alltiers=leaguetiers.objects.all().filter(league=league_).exclude(tiername=tiername).order_by('-tierpoints')
    except:
        messages.error(request,'Tier does not exist!',extra_tags='danger')
        return redirect('league_tiers',league_name=league_name)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'tier': tiername,
        'tiers':tiers,
        'alltiers': alltiers,
    }
    return render(request, 'individualtier.html',context)

def available_league_tiers(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    tiers=leaguetiers.objects.all().filter(league=league_).order_by('-tierpoints')
    mega=[]
    tierlist=[]
    banned=False
    for item in tiers:
        tieritems=[]
        tieritems_=pokemon_tier.objects.all().filter(tier=item).order_by('pokemon__pokemon')
        for pokemon in tieritems_:
            try:    
                rosterspot=roster.objects.all().filter(season=season).get(pokemon=pokemon.pokemon)
                team=rosterspot.team
            except:
                team=None
                tieritems.append([pokemon,team])
        if item.tiername.find("Mega")>-1:
            mega.append([item,tieritems])   
        elif item.tiername.find("Banned")>-1:
            banned=True 
        else:
            tierlist.append([item,tieritems]) 
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'tiers': tierlist,
        'mega': mega,
        'banned': banned,
        'availabletiers': True,
    }
    return render(request, 'tiers.html',context)

def available_individual_league_tier(request,league_name,tiername):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    try:
        tiername=tiername.replace("_"," ")
        tierofinterest=leaguetiers.objects.all().filter(league=league_).get(tiername=tiername)
        tiers=[]
        tiers_=pokemon_tier.objects.all().filter(tier=tierofinterest).order_by('pokemon__pokemon')
        for item in tiers_:
            try:    
                rosterspot=roster.objects.all().filter(season=season).get(pokemon=item.pokemon)
                team=rosterspot.team
            except:
                team=None
                tiers.append([item,team])
        alltiers=leaguetiers.objects.all().filter(league=league_).exclude(tiername=tiername).order_by('-tierpoints').exclude(tiername='Banned')
    except:
        messages.error(request,'Tier does not exist!',extra_tags='danger')
        return redirect('league_tiers',league_name=league_name)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'tier': tiername,
        'tiers':tiers,
        'alltiers': alltiers,
        'availabletiers': True,
    }
    return render(request, 'individualtier.html',context)

@login_required
def freeagency(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    coach=coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user)).first()
    coachroster=all_pokemon.objects.all().order_by('pokemon')
    for item in coachroster:
        try:
            roster.objects.all().filter(season=season,team=coach).get(pokemon=item)
        except:
            coachroster=coachroster.exclude(pokemon=item.pokemon)
    availablepokemon=all_pokemon.objects.all().order_by('pokemon')
    for item in availablepokemon:
        try:
            roster.objects.all().filter(season=season).get(pokemon=item)
            availablepokemon=availablepokemon.exclude(pokemon=item.pokemon)
        except:
            tier=pokemon_tier.objects.all().filter(league=league_).get(pokemon=item)
            if tier.tier.tiername=="Banned":
                availablepokemon=availablepokemon.exclude(pokemon=item.pokemon)
            available=True
    if request.method=="POST":
        form=FreeAgencyForm(coachroster,availablepokemon,request.POST)
        if form.is_valid():
            droppedpokemon=roster.objects.filter(season=season,team=coach).get(pokemon=form.cleaned_data['droppedpokemon'])
            droppedpokemon.kills=0
            droppedpokemon.deaths=0
            droppedpokemon.gp=0
            droppedpokemon.gw=0
            droppedpokemon.differential=0
            droppedpokemon.zuser="N"
            droppedpokemon.pokemon=form.cleaned_data['addedpokemon']
            droppedpokemon.save()
            form.save()
            messages.success(request,f'You free agency request has been implemented!')
            return redirect('team_page',league_name=league_name,team_abbreviation=droppedpokemon.team.teamabbreviation)
    form=FreeAgencyForm(coachroster,availablepokemon,initial={'coach':coach,'season':season})
    fa_remaining=season.freeagenciesallowed-free_agency.objects.all().filter(season=season,coach=coach).count()
    if fa_remaining < 1:
        messages.error(request,'You do not have any free agencies remaining!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'form':form,
        'fa_remaining':fa_remaining,
    }
    return render(request, 'freeagency.html',context)

@login_required
def league_leaders(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    
    leagueleaders=roster.objects.all().filter(season=season,gp__gt=0).order_by('-kills','-differential')
    
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'leagueleaders': leagueleaders,
    }
    return render(request, 'leagueleaders.html',context)

@login_required
def trading_view(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    coach=coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user)).first()
    coachroster=roster.objects.all().filter(season=season,team=coach).order_by('pokemon__pokemon')
    availablepokemon=roster.objects.all().filter(season=season).exclude(team=coach).order_by('pokemon__pokemon')
    if request.method=="POST":
        form=TradeRequestForm(coachroster,availablepokemon,request.POST)
        if form.is_valid():
            traderequest=form.save()
            sender=traderequest.offeredpokemon.team.coach
            recipient=traderequest.requestedpokemon.team.coach
            messagebody=f"Hello,\nI would like to trade my {traderequest.offeredpokemon.pokemon.pokemon} for your {traderequest.requestedpokemon.pokemon.pokemon}."
            inbox.objects.create(sender=sender,recipient=recipient,messagesubject="Trade Request",messagebody=messagebody,traderequest=traderequest)
            messages.success(request,f'Your trade request has been sent!')
    form=TradeRequestForm(coachroster,availablepokemon)
    trade_remaining=season.tradesallowed-trading.objects.all().filter(coach=coach).count()
    if trade_remaining < 1:
        messages.error(request,'You do not have any trades remaining!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'form':form,
        'trade_remaining':trade_remaining,
    }
    return render(request, 'trading.html',context)