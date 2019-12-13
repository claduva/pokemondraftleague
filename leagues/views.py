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

from datetime import datetime, timezone, timedelta
import pytz
import math
import random

from .forms import *
from .models import *
from leagues.models import league_team
from pokemondatabase.models import *
from pokemonadmin.models import *
from individualleague.models import *
from accounts.models import *
from pokemondraftleague.customdecorators import check_if_subleague, check_if_league, check_if_season, check_if_team, check_if_host

@login_required
def create_league(request):
    if request.method == 'POST':
        form = CreateLeagueForm(request.POST)
        if form.is_valid():
            newleague=form.save()
            newleague.host.add(request.user)
            newleague.save()
            messages.success(request,f'Your league has been successfully created!')
            return redirect('league_list')
        else:
            print(form.errors)
    else:
        form = CreateLeagueForm(initial={'host': request.user})
    context = {
        'form': form,
    }
    return render(request, 'createleague.html',context)

def league_list(request):
    context={
        'leagueheading': 'All Leagues',
    }
    return render(request, 'leagues.html',context)

@login_required
def leagues_hosted_settings(request):
    context = {
        'settingheading': "Select League",
        'leagueshostedsettings': True,
    }
    return render(request, 'leaguelist.html',context)

@check_if_league
@check_if_host
@login_required
def individual_league_settings(request,league_name):
    league_instance=league.objects.get(name=league_name)
    league_settings_instance=league_settings.objects.get(league_name=league_instance)
    if request.method == 'POST':
        l_form = UpdateLeagueForm(
            request.POST,
            request.FILES,
            instance=league_instance
            )
        ls_form = UpdateLeagueSettingsForm(request.POST,instance=league_settings_instance)
        if l_form.is_valid() and ls_form.is_valid():
            l_form.save()
            ls_form.save()
            messages.success(request,league_name+' has been updated!')
            return redirect('individual_league_settings',league_name=league_name)
    else:
        l_form = UpdateLeagueForm(instance=league_instance)
        ls_form = UpdateLeagueSettingsForm(instance=league_settings_instance)
    addleagueteam=league_settings_instance.teambased
    context = {
        'settingheading': league_name,
        'forms': [l_form,ls_form],
        'deletebutton': 'Delete League',
        'leagueshostedsettings': True,
        'addleagueteam': addleagueteam,
        'league_name':league_name,
    }
    return render(request, 'settings.html',context)

@check_if_league
@check_if_host
@login_required
def league_configuration_(request,league_name):
    league_instance=league.objects.get(name=league_name)
    if request.method == 'POST':
        formpurpose=request.POST['purpose']
        if formpurpose=="Submit":
            try:
                existingconfiguration=league_instance.configuration
                numsubleagues=existingconfiguration.number_of_subleagues
                form=LeagueConfigurationForm(request.POST,instance=existingconfiguration)
            except:
                form=LeagueConfigurationForm(request.POST)
                numsubleagues=None
            if form.is_valid():
                config=form.save()
                newnumsubleagues=config.number_of_subleagues
                if newnumsubleagues != numsubleagues:
                    try:
                        league_instance.subleague.all().delete()
                    except:
                        pass
                    pokemon_tier.objects.filter(league=league_instance).all().delete()
                    if config.number_of_subleagues==1:
                        sl=league_subleague.objects.create(league=league_instance,subleague="Main")
                        allpokes=all_pokemon.objects.all()
                        i=pokemon_tier.objects.all().order_by('id').last().id
                        bannedtier=leaguetiers.objects.create(league=league_instance,subleague=sl,tiername="Banned",tierpoints=1000)
                        for item in allpokes:
                            i+=1
                            pokemon_tier.objects.create(id=i,pokemon=item,league=league_instance,subleague=sl,tier=bannedtier)
                    elif config.number_of_subleagues>1:
                        for i in range(config.number_of_subleagues):
                            sl=league_subleague.objects.create(league=league_instance,subleague=f"Subleague{i+1}")
                            allpokes=all_pokemon.objects.all()
                            i=pokemon_tier.objects.all().order_by('id').last().id
                            bannedtier=leaguetiers.objects.create(league=league_instance,subleague=sl,tiername="Banned",tierpoints=1000)
                            for item in allpokes:
                                i+=1
                                pokemon_tier.objects.create(id=i,pokemon=item,league=league_instance,subleague=sl,tier=bannedtier)
                    messages.success(request,league_name+' has been updated!')
        elif formpurpose=="Rename":
            itemid=request.POST['itemid']
            slname=request.POST['slname']
            print(slname)
            i=league_subleague.objects.get(id=int(itemid))
            i.subleague=slname
            i.save()
    try:
        existingconfiguration=league_instance.configuration
        form=LeagueConfigurationForm(initial={'league':league_instance},instance=existingconfiguration)
    except:
        form=LeagueConfigurationForm(initial={'league':league_instance})
    showsubleagues=False
    try:    
        subleagues=league_instance.subleague.all()
        if subleagues.count()>1:
            showsubleagues=True
    except:
        subleagues=None
    context = {
        'league_name': league_name,
        'settingheading': league_name,
        'leagueshostedsettings': True,
        'form':form,
        'subleagues':subleagues,
        'showsubleagues':showsubleagues,
    }
    return render(request, 'leagueconfiguration.html',context)

@check_if_subleague
@check_if_host
@login_required
def discordsettings(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    try:
        discordinstance=discord_settings.objects.get(subleague=subleague)
        form=DiscordSettingsForm(instance=discordinstance)
        if request.method=='POST':
            form=DiscordSettingsForm(request.POST,instance=discordinstance)
            if form.is_valid():
                form.save()
                messages.success(request,league_name+' has been updated!')
            else:
                messages.error(request,'Form invalid!')
            return redirect('manage_seasons',league_name=league_name,subleague_name=subleague_name)
    except Exception as e:
        form=DiscordSettingsForm(initial={'league':subleague.league,'subleague':subleague,})
        if request.method=='POST':
            form=DiscordSettingsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,league_name+' has been updated!')
            else:
                messages.error(request,'Form invalid!')
            return redirect('manage_seasons',league_name=league_name,subleague_name=subleague_name)
    context = {
        'settingheading': f'{subleague} Discord Settings',
        'forms': [form],
        'leagueshostedsettings': True,
    }
    return render(request, 'formsettings.html',context)

@check_if_league
@check_if_host
@login_required
def manage_coachs(request,league_name):
    league_name=league_name.replace("_"," ")
    league_=league.objects.get(name=league_name)
    applicants=league_application.objects.filter(league_name=league_)
    totalapplicants=len(applicants)
    coachs=coachdata.objects.filter(league_name=league_).order_by('coach__username')
    spotsremaining=True
    context = {
        'applicants': applicants,
        'coachs': coachs,
        'league_name': league_name,
        'leagueshostedsettings': True,
        'totalapplicants': totalapplicants,
        'spotsremaining': spotsremaining,
        'league': league_,
    }
    return render(request, 'managecoachs.html',context)

@login_required
def view_application(request,league_name):
    if request.POST:
        formpurpose=request.POST['purpose']
        if formpurpose=="View":
            application=league_application.objects.get(pk=request.POST['coach'])
            context = {
                'league_name': league_name,
                'leagueshostedsettings': True,
                "appofinterest":application,
            }
            return render(request, 'view_application.html',context)
        elif formpurpose=="Delete Application":
            league_application.objects.get(id=request.POST['appid']).delete()
            messages.success(request,'Application has been deleted!')
        elif formpurpose=="Add to Subleague":
            appofinterest=league_application.objects.get(id=request.POST['appid'])
            subleagueofinterest=league_subleague.objects.get(id=request.POST['subleagueid'])
            coachdata.objects.create(
                coach=appofinterest.applicant,
                league_name=appofinterest.league_name,
                subleague=subleagueofinterest,
                teamabbreviation=appofinterest.teamabbreviation,
                teamname=appofinterest.teamname,
                )
            appofinterest.delete()
            messages.success(request,'Coach has been added!')
    return redirect('manage_coachs',league_name=league_name)

@login_required
def remove_coach(request,league_name):
    if request.POST:
        league_=league.objects.get(name=league_name)
        try:
            seasonsetting.objects.get(league=league_)
            messages.error(request,'The season has already started!',extra_tags='danger')
            return redirect('manage_coachs',league_name=league_name)
        except:
            coachtoremove=coachdata.objects.get(pk=request.POST['coachtoupdate'])
            league_application.objects.create(applicant=coachtoremove.coach,league_name=coachtoremove.league_name)
            coachtoremove.delete()
    return redirect('manage_coachs',league_name=league_name)

@login_required
def leagues_coaching_settings(request):
    context = {
        'settingheading': "Select League",
        'leaguescoachingpage': True,
        'leaguescoachingsettings': True,
    }
    return render(request, 'leaguelist.html',context)

@login_required
def individual_league_coaching_settings(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
        coachinstance=coachdata.objects.filter(league_name=league_instance).filter(Q(coach=request.user)|Q(teammate=request.user)).first()
        settings=league_settings.objects.get(league_name=league_instance)
        allowsteams=settings.allows_teams
        teambased=settings.teambased
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        if allowsteams:
            form = UpdateCoachInfoForm(
                request.POST,
                request.FILES,
                instance=coachinstance
                )
            tm_form=UpdateCoachTeammateForm(request.POST,instance=coachinstance)
            if teambased:
                parent_team_form=UpdateParentTeamForm(league_instance,request.POST,instance=coachinstance)
                if form.is_valid() and tm_form.is_valid() and parent_team_form.is_valid():
                    form.save()
                    tm_form.save()
                    parent_team_form.save()
                    messages.success(request,'Your coach info has been updated!')
                    return redirect('individual_league_coaching_settings',league_name=league_name)
            else:    
                if form.is_valid() and tm_form.is_valid():
                    form.save()
                    tm_form.save()
                    messages.success(request,'Your coach info has been updated!')
                    return redirect('individual_league_coaching_settings',league_name=league_name)
        else:
            form = UpdateCoachInfoForm(
                request.POST,
                request.FILES,
                instance=coachinstance
                )
            if teambased:
                parent_team_form=UpdateParentTeamForm(league_instance,request.POST,instance=coachinstance)
                if form.is_valid() and parent_team_form.is_valid():
                    form.save()
                    parent_team_form.save()
                    messages.success(request,'Your coach info has been updated!')
                    return redirect('individual_league_coaching_settings',league_name=league_name)
            else:
                if form.is_valid():
                    form.save()
                    messages.success(request,'Your coach info has been updated!')
                    return redirect('individual_league_coaching_settings',league_name=league_name)
    else:
        form = UpdateCoachInfoForm(instance=coachinstance)
        forms=[]
        forms.append(form)
        if teambased:
            parent_team_form=UpdateParentTeamForm(league_instance,instance=coachinstance)
            forms.append(parent_team_form)
        if allowsteams:
            tm_form=UpdateCoachTeammateForm(instance=coachinstance)
            forms.append(tm_form)

    context = {
        'settingheading': league_name,
        'forms': forms,
        'leaguescoachingsettings': True,
        'league_name':league_name,
    }
    return render(request, 'settings.html',context)

@check_if_subleague
@check_if_host
@login_required
def manage_seasons(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    seasonsettings=seasonsetting.objects.get(subleague=subleague)
    needednumberofcoaches=seasonsettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=subleague.league)
    currentcoachescount=len(currentcoaches)
    #if needednumberofcoaches != currentcoachescount: 
    #    messages.error(request,'You can only utilize season settings if you have designated the same number of coaches as available spots',extra_tags='danger')
    #    return redirect('individual_league_settings',league_name=league_name)
    if request.method == 'POST':
        try:
            
            form = EditSeasonSettingsForm(request.POST,instance=seasonsettings)
            if form.is_valid():
                form.save()
                messages.success(request,'Season settings have been updated!')
            else:
                messages.error(request,form.errors,extra_tags='danger')    
        except:   
            form = CreateSeasonSettingsForm(request.POST)
            print('here') 
            if form.is_valid():
                thisseason=form.save()
                picksperteam=form.cleaned_data['picksperteam']
                rosterid=roster.objects.all().order_by('id').last().id
                for coach in currentcoaches:
                    for i in range(picksperteam):
                        rosterid+=1
                        roster.objects.create(id=rosterid,season=thisseason,team=coach)
                rule.objects.create(season=thisseason)
                messages.success(request,'Your season has been created!')
        return redirect('manage_seasons',league_name=league_name,subleague_name=subleague_name)
    else:
        try:
            seasonsettings=seasonsetting.objects.get(subleague=subleague)
            form = EditSeasonSettingsForm(instance=seasonsettings)
            settingheading='Update Season Settings'
            create=False
            manageseason=True
        except:
            seasonsettings=None
            form = CreateSeasonSettingsForm(initial={'league': subleague.league,'subleague':subleague})
            settingheading='Create New Season'
            create=True
            manageseason=False
    context = {
        'subleague':subleague,
        'league_name': league_name,
        'leagueshostedsettings': True,
        'forms': [form],
        'seasonsettings': seasonsettings,
        'settingheading': settingheading,
        'create': create,
        'manageseason': manageseason,    
    }
    return render(request, 'settings.html',context)

#works
@check_if_subleague
@check_if_host
@login_required
def manage_tiers(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    if request.method == 'POST':
        form = CreateTierForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been added!')
            return redirect('manage_tiers',league_name=league_name,subleague_name=subleague_name)
    else:
        form = CreateTierForm(initial={'league': subleague.league,'subleague':subleague})
    pokemontiers=pokemon_tier.objects.filter(subleague=subleague).all().order_by('pokemon__pokemon','tier')
    leaguestiers=leaguetiers.objects.filter(subleague=subleague).all().order_by('tiername')
    untiered=pokemon_tier.objects.filter(subleague=subleague,tier=None).all().order_by('pokemon__pokemon')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'managetiers': True,
        'subleague':subleague,
        'untiered':untiered,
    }
    return render(request, 'managetiers.html',context)

@csrf_exempt
def update_tiering(request):
    tierid=request.POST['tierid']
    pokemonid=request.POST['pokemonid']
    newtierid=request.POST['newtierid']
    newtier=leaguetiers.objects.get(id=newtierid)
    if tierid != "Untiered":
        poi=pokemon_tier.objects.get(id=tierid)
        poi.tier=newtier
        poi.save()
    else:
        poi=pokemon_tier.objects.get(id=pokemonid)
        poi.tier=newtier
        poi.save()
    data={
        'response':'Success'
        }
    return JsonResponse(data)

#works
@login_required
def delete_tier(request,league_name,subleague_name):
    if request.POST:
        tiertodelete=leaguetiers.objects.get(pk=request.POST['tiertodelete']).delete()
    return redirect('manage_tiers',league_name=league_name,subleague_name=subleague_name)

#works
@check_if_subleague
@check_if_host
@login_required
def edit_tier(request,league_name,subleague_name,tierid):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    if request.method == 'POST':
        tierinstance=leaguetiers.objects.get(pk=tierid)
        form = UpdateTierForm(request.POST,instance=tierinstance)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been edited!')
            return redirect('manage_tiers',league_name=league_name,subleague_name=subleague_name)
    else:
        tierinstance=leaguetiers.objects.get(pk=tierid)
        form=UpdateTierForm(instance=tierinstance)
    pokemontiers=pokemon_tier.objects.filter(subleague=subleague).all().order_by('pokemon__pokemon','tier__tierpoints')
    leaguestiers=leaguetiers.objects.filter(subleague=subleague).all().order_by('tiername')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'editingtier': True,
        'subleague':subleague,
    }
    return render(request, 'managetiers.html',context)

#works
@check_if_subleague
@check_if_host
@login_required
def update_tier(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_=subleague.league
    if request.POST:
        pokemonofinterest=all_pokemon.objects.get(pokemon=request.POST['pokemon-select'])
        pokemontoupdate=pokemon_tier.objects.filter(subleague=subleague).get(pokemon=pokemonofinterest)
        tiertoadd=leaguetiers.objects.get(pk=request.POST['tier-select'])
        pokemontoupdate.tier=tiertoadd
        pokemontoupdate.save()
        messages.success(request,'Tier has been edited!')
    return redirect('manage_tiers',league_name=league_name,subleague_name=subleague_name)

#works
@check_if_subleague
@check_if_host
@login_required
def view_tier(request,league_name,subleague_name,tier):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_=subleague.league
    if request.method == 'POST':
        form = CreateTierForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been added!')
            return redirect('manage_tiers',league_name=league_name,subleague_name=subleague_name)
    else:
        form = CreateTierForm(initial={'league': league_,',subleague':subleague})
        pokemontiers=pokemon_tier.objects.filter(subleague=subleague).all().order_by('pokemon__pokemon','tier')
        leaguestiers=leaguetiers.objects.filter(subleague=subleague).all().order_by('tiername')
        if tier=="Untiered":
            pokemonlist=pokemon_tier.objects.filter(subleague=subleague,tier=None).all().order_by('pokemon__pokemon')
        else:
            tier=tier.replace("_"," ")
            tierofinterest=leaguetiers.objects.filter(subleague=subleague,tiername=tier).first()
            pokemonlist=pokemon_tier.objects.filter(subleague=subleague,tier=tierofinterest).all().order_by('pokemon__pokemon')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'pokemonlist': pokemonlist,
        'subleague':subleague,
    }
    return render(request, 'managetiers.html',context)


@check_if_subleague
@check_if_host
@login_required
def default_tiers(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_=subleague.league
    if request.method == 'POST':
        purpose=request.POST['purposeid']
        if purpose=='Select':
            templatetierset=leaguetiertemplate.objects.all().exclude(tiername="Banned").filter(template=request.POST['template-select'])
            leaguetiers.objects.all().filter(subleague=subleague).exclude(tiername="Banned").delete()
            for item in templatetierset:
                leaguetiers.objects.create(league=league_,subleague=subleague,tiername=item.tiername,tierpoints=item.tierpoints)
            templatepokemonset=pokemon_tier_template.objects.all().exclude(tier__tiername="Banned").filter(template=request.POST['template-select'])
            existingpokemontiers=pokemon_tier.objects.all().filter(league=league_,subleague=subleague)
            thisleaguetiers=leaguetiers.objects.all().filter(subleague=subleague)
            for item in templatepokemonset:
                tiertouse=thisleaguetiers.get(tiername=item.tier.tiername)
                mtu=existingpokemontiers.get(pokemon=item.pokemon)
                mtu.tier=tiertouse
                mtu.save()
            messages.success(request,'The template has been applied!')
        elif purpose=="Use":
            #delete existing
            subleague.subleaguetiers.all().exclude(tiername="Banned").delete()
            #add new
            leagueofinterest=league_subleague.objects.get(id=request.POST['leagueid'])
            leagueofinteresttiers=leagueofinterest.subleaguetiers.all().exclude(tiername="Banned")
            for item in leagueofinteresttiers:
                leaguetiers.objects.create(league=league_,subleague=subleague,tiername=item.tiername,tierpoints=item.tierpoints)
            leagueofinteresttiering=leagueofinterest.subleaguepokemontiers.all().exclude(tier__tiername="Banned")
            existingpokemontiers=pokemon_tier.objects.all().filter(league=league_,subleague=subleague)
            thisleaguetiers=leaguetiers.objects.all().filter(subleague=subleague)
            for item in leagueofinteresttiering:
                tiertouse=thisleaguetiers.get(tiername=item.tier.tiername)
                mtu=existingpokemontiers.get(pokemon=item.pokemon)
                mtu.tier=tiertouse
                mtu.save()
        return redirect('manage_tiers',league_name=league_name,subleague_name=subleague_name)
    else:
        pokemonlist=pokemon_tier.objects.filter(subleague=subleague,tier=None).all().order_by('pokemon__pokemon')
        pokemontiers=pokemon_tier.objects.filter(subleague=subleague).all().order_by('pokemon__pokemon','tier')
        leaguestiers=leaguetiers.objects.filter(subleague=subleague).all().order_by('tiername')
        availabletemplates=leaguetiertemplate.objects.all().distinct('template')
        form = CreateTierForm(initial={'league': league_,'subleague': subleague})
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'pokemonlist': pokemonlist,
        'defaulttemplate': True,
        'availabletemplates': availabletemplates,
        'subleague':subleague,
    }
    return render(request, 'managetiers.html',context)

@check_if_subleague
@check_if_season
@check_if_host
@login_required
def set_draft_order(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_=subleague.league
    leaguesettings=league_settings.objects.get(league_name=league_)
    currentcoaches=coachdata.objects.filter(subleague=subleague).order_by('teamname')
    currentcoachescount=len(currentcoaches)
    seasonsettings=seasonsetting.objects.filter(subleague__league__name=league_name).get(subleague__subleague=subleague_name)
    needednumberofcoaches=seasonsettings.number_of_teams
    draftstyle=seasonsettings.drafttype  
    if request.method == 'POST':
        formpurpose=request.POST['formpurpose']
        if formpurpose=='Set':
            currentdraft=draft.objects.all().filter(season=seasonsettings).delete()
            currentroster=roster.objects.all().filter(season=seasonsettings).delete()
            if draftstyle=="Snake":
                order=[]
                for i in range(needednumberofcoaches):
                    order.append(coachdata.objects.filter(teamname=request.POST[str(i+1)],subleague=subleague).first())
                flippedorder=order[::-1]
                numberofpicks=seasonsettings.picksperteam
                id_=roster.objects.all().order_by('-id').first().id
                for i in range(numberofpicks):
                    if i%2 == 0:
                        for item in order:
                            id_+=1
                            draft.objects.create(season=seasonsettings,team=item)
                            roster.objects.create(id=id_,season=seasonsettings,team=item)
                    else:    
                        for item in flippedorder:
                            id_+=1
                            draft.objects.create(season=seasonsettings,team=item)
                            roster.objects.create(id=id_,season=seasonsettings,team=item)
        elif formpurpose=='Randomize':
            currentdraft=draft.objects.all().filter(season=seasonsettings).delete()
            currentroster=roster.objects.all().filter(season=seasonsettings).delete()
            coachstoadd=coachdata.objects.all().filter(subleague=subleague)
            order=[]
            for item in coachstoadd:
                order.append(item)
            random.shuffle(order)
            flippedorder=order[::-1]
            numberofpicks=seasonsettings.picksperteam
            id_=roster.objects.all().order_by('id').last().id
            for i in range(numberofpicks):
                if i%2 == 0:
                    for item in order:
                        id_+=1
                        draft.objects.create(season=seasonsettings,team=item)
                        roster.objects.create(id=id_,season=seasonsettings,team=item)
                else:    
                    for item in flippedorder:
                        id_+=1
                        draft.objects.create(season=seasonsettings,team=item)
                        roster.objects.create(id=id_,season=seasonsettings,team=item)
        messages.success(request,'Draft order has been set!')
        return redirect('individual_league_settings',league_name=league_name)        
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'settingheading': 'Set Draft Order',
        'currentcoaches': currentcoaches,
        'subleague':subleague,
    }
    return render(request, 'draftorder.html',context)

@check_if_subleague
@check_if_host
@login_required
def add_conference_and_division_names(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_=subleague.league
    leaguesettings=seasonsetting.objects.get(subleague=subleague)
    currentconferences = conference_name.objects.all().filter(subleague=subleague)
    currentdivisions = division_name.objects.all().filter(subleague=subleague)
    totalconferences=leaguesettings.number_of_conferences
    totaldivisions=leaguesettings.number_of_divisions
    neededconferences=totalconferences-currentconferences.count()
    neededdivisions=totaldivisions-currentdivisions.count()
    if int(totalconferences/totaldivisions)==1:
        neededdivisions=0 
    if request.method == 'POST':
        name=request.POST['itemname']
        category=request.POST['category']
        if category=='conference':
            conference_name.objects.create(league=league_,subleague=subleague,name=name)
        elif category=='division':
            associatedconference=conference_name.objects.all().filter(subleague=subleague).get(name=request.POST['divisionconference'])
            division_name.objects.create(league=league_,subleague=subleague,name=name,associatedconference=associatedconference)
        messages.success(request,f'{name} has been added as a {category}!')
        return redirect('add_conference_and_division_names',league_name=league_name,subleague_name=subleague_name)        
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'currentconferences': currentconferences,
        'currentdivisions': currentdivisions,
        'neededconferences': neededconferences,
        'neededdivisions': neededdivisions,
        'subleague':subleague,
    }
    return render(request, 'addconferencesanddivisions.html',context)

@login_required
def delete_conference(request,league_name,subleague_name):
    if request.method=="POST":
        itemid=request.POST['itemid']
        itemtodelete=conference_name.objects.get(pk=itemid)
        itemtodelete.delete()
        messages.success(request,'Conference has been deleted!')
    return redirect('add_conference_and_division_names',league_name=league_name,subleague_name=subleague_name)        

@login_required
def delete_division(request,league_name,subleague_name):
    if request.method=="POST":
        itemid=request.POST['itemid']
        itemtodelete=division_name.objects.get(pk=itemid)
        itemtodelete.delete()
        messages.success(request,'Division has been deleted!')
    return redirect('add_conference_and_division_names',league_name=league_name,subleague_name=subleague_name)        

@check_if_league
@check_if_host
@login_required
def manage_coach(request,league_name,coachofinterest):
    league_name=league_name.replace("_"," ")
    league_=league.objects.get(name=league_name.replace("_"," "))
    try:
        coachofinterest=coachdata.objects.filter(league_name=league_).get(coach__username=coachofinterest)
    except:
        messages.error(request,'Coach does not exist!',extra_tags='danger')
        league_name=league_name.replace(" ","_")
        return redirect('manage_coachs', league_name=league_name)
    form=ManageCoachForm(league_,coachofinterest.subleague,instance=coachofinterest)
    try:
        season=seasonsetting.objects.get(league=league_)
        seasonnotinsession=False
    except:
        seasonnotinsession=True
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'coachofinterest':coachofinterest,
    } 
    if request.method == 'POST':
        formtype=request.POST['formtype']
        coachtoupdate=coachdata.objects.get(id=request.POST['coachtoupdate'])
        print(coachtoupdate)
        if formtype=="Update":
            form=ManageCoachForm(league_,coachtoupdate.subleague,request.POST,request.FILES,instance=coachtoupdate)
            if form.is_valid():
                form.save()
                messages.success(request,f'{coachofinterest.coach.username} has been updated!')
                return redirect('manage_coachs', league_name=league_name)
        elif formtype=="Adjust Draft":
            context.update({
                'coachtoupdate':coachtoupdate,
                'adjustdraft': True,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="Adjust Roster":
            context.update({
                'coachtoupdate':coachtoupdate,
                'adjustroster': True,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="Update Draft":
            pokemontoupdate=draft.objects.get(id=request.POST['pokemontoupdate'])
            try:
                pokemontoupdateto=all_pokemon.objects.get(pokemon=request.POST['pokemontoupdateto'])
                pokemontoupdate.pokemon=pokemontoupdateto
                pokemontoupdate.save()
                messages.success(request,"Draft has been updated")
            except Exception as e:
                print(e)
                messages.error(request,"Pokemon doesn't exist",extra_tags="danger")
            return redirect('manage_coachs', league_name=league_name)
        elif formtype=="Update Roster":
            pokemontoupdate=roster.objects.get(id=request.POST['pokemontoupdate'])
            try:
                pokemontoupdateto=all_pokemon.objects.get(pokemon=request.POST['pokemontoupdateto'])
                pokemontoupdate.pokemon=pokemontoupdateto
                pokemontoupdate.save()
                messages.success(request,"Roster has been updated")
            except Exception as e:
                print(e)
                messages.error(request,"Pokemon doesn't exist",extra_tags="danger")
            return redirect('manage_coachs', league_name=league_name)
        elif formtype=="Adjust Record":
            context.update({
                'form': UpdateCoachRecordForm(instance=coachtoupdate),
                'coachtoupdate':coachtoupdate,
                'adjustrecord': True,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="updatecoachdata":
            form=UpdateCoachRecordForm(request.POST,instance=coachtoupdate)
            if form.is_valid():
                form.save()
                messages.success(request,f'{coachtoupdate.coach.username} has been updated!')
                return redirect('manage_coachs', league_name=league_name)
            return redirect('manage_coachs', league_name=league_name)
        elif formtype=="Add Showdown Alt":
            alts=showdownalts.objects.all().filter(user=coachtoupdate.coach)
            context.update({
                'alts':alts,
                'coachtoupdate':coachtoupdate,
                'addalt': True,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="addalt":
            showdownalts.objects.create(user=coachtoupdate.coach,showdownalt=request.POST['givenalt'])
            messages.success(request,f'{coachtoupdate.coach} has been updated!')
            return redirect('manage_coachs', league_name=league_name)     
    context.update({
        'form':form,
        'coachform':True,
        'seasonnotinsession': seasonnotinsession,
    })
    return render(request, 'managecoach.html',context)

@check_if_league
@login_required
def designate_z_users(request,league_name):
    league_instance=league.objects.get(name=league_name)
    coachinstance=coachdata.objects.filter(league_name=league_instance).filter(Q(coach=request.user)|Q(teammate=request.user)).first()
    settings=league_settings.objects.get(league_name=league_instance)
    season=coachinstance.subleague.seasonsetting
    if request.method == 'POST':
        form=DesignateZUserForm(season,coachinstance,request.POST)
        if form.is_valid():
            zuser=form.cleaned_data['zuser']
            ztype=form.cleaned_data['zmovetype']
            zuser.zuser=ztype
            zuser.save()
            messages.success(request,f'{zuser.pokemon.pokemon} has been added as a Z user!')
        return redirect('designate_z_users',league_name=league_name)
    else:
        numberofz=season.numzusers
        currentz=roster.objects.all().filter(season=season,team=coachinstance).exclude(zuser="N")
        zneeded=numberofz-currentz.count()
        forms=[]
        forms.append(DesignateZUserForm(season,coachinstance))
    context = {
        'settingheading': f'{league_name}: Designate Z Users',
        'leaguescoachingsettings': True,
        'league_name':league_name,
        'forms': forms,
        'zneeded':zneeded,
        'currentz': currentz,
        'candeletez': season.candeletez,
    }
    return render(request, 'designatezusers.html',context)

@check_if_league
@login_required
def delete_z_user(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
        coachinstance=coachdata.objects.filter(league_name=league_instance).filter(Q(coach=request.user)|Q(teammate=request.user)).first()
        settings=league_settings.objects.get(league_name=league_instance)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_coaching_settings')
    try:
        season=coachinstance.subleague.seasonsetting
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('leagues_coaching_settings')
    if request.method == 'POST':
        
        zuser=roster.objects.get(pk=request.POST['zid'])
        zuser.zuser="N"
        zuser.save()
        messages.success(request,f'{zuser.pokemon.pokemon} has been removed as a Z user!')
    print("here")
    return redirect('designate_z_users',league_name=league_name)

@login_required
def add_team_of_coachs(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
        coachinstance=coachdata.objects.filter(league_name=league_instance).filter(Q(coach=request.user)|Q(teammate=request.user)).first()
        settings=league_settings.objects.get(league_name=league_instance)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_coaching_settings')
    heading='Add Team of Coaches'
    if request.method == 'POST':
        purpose=request.POST['purpose']
        if purpose == 'Submit':
            form=AddTeamOfCoachsForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,f'Team has been added!')
        elif purpose == 'Delete':
            teamtodelete=league_team.objects.get(id=request.POST['deleteid'])
            teamtodelete.delete()
        elif purpose == 'Edit':
            team_instance=league_team.objects.get(id=request.POST['editid'])
            editid=team_instance.id
            form=AddTeamOfCoachsForm(instance=team_instance)
            allteams=league_team.objects.all().filter(league=league_instance)
            heading='Edit Team of Coaches'
            context = {
                'leagueshostedsettings': True,
                'league_name':league_name,
                'form': form,
                'allteams': allteams,
                'heading':heading,
                'updateteam': True,
                'editid': editid,
            }
            return render(request, 'addteamofcoachs.html',context)
        elif purpose == 'Update':
            team_instance=league_team.objects.get(id=request.POST['editid'])
            form=AddTeamOfCoachsForm(request.POST,request.FILES,instance=team_instance)
            if form.is_valid():
                form.save()
                messages.success(request,f'Team has been updated!')
    form=AddTeamOfCoachsForm(initial={'league':league_instance})
    allteams=league_team.objects.all().filter(league=league_instance)
    context = {
        'leagueshostedsettings': True,
        'league_name':league_name,
        'form': form,
        'heading':heading,
        'allteams': allteams,
    }
    return render(request, 'addteamofcoachs.html',context)

@check_if_league
@check_if_host
@login_required
def archive_season(request,league_name):
    league_=league.objects.get(name=league_name)
    unplayedgames=schedule.objects.all().filter(replay="Link",season__league=league_).count()
    if unplayedgames>0:
        messages.error(request,'You cannot archive a season with matches remaining to be played!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    coachdataitems=coachdata.objects.all().filter(league_name=league_)
    rosteritems=roster.objects.all().filter(season__league=league_)
    draftitems=draft.objects.all().filter(season__league=league_)
    scheduleitems=schedule.objects.all().filter(season__league=league_)
    freeagencyitems=free_agency.objects.all().filter(season__league=league_)
    tradingitems=trading.objects.all().filter(season__league=league_)
    season=league_.subleague.first().seasonsetting
    maxid=historical_team.objects.all().order_by('-id').first().id
    for item in coachdataitems:
        maxid+=1
        if item.teammate:
            historical_team.objects.create(
                id=maxid,
                league = item.league_name,
                seasonname = season.seasonname,
                teamname = item.teamname,
                coach1= item.coach,
                coach1username=item.coach.username,
                coach2=item.teammate,
                coach2username=item.teammate.username,
                logo = item.logo,
                wins=item.wins,
                losses=item.losses,
                differential=item.differential,
                forfeit=item.forfeit,
                support=item.support,
                damagedone=item.damagedone,
                hphealed=item.hphealed,
                luck=item.luck,
                remaininghealth=item.remaininghealth
            )
        else:
            historical_team.objects.create(
                id=maxid,
                league = item.league_name,
                seasonname = season.seasonname,
                teamname = item.teamname,
                coach1= item.coach,
                coach1username=item.coach.username,
                logo = item.logo,
                wins=item.wins,
                losses=item.losses,
                differential=item.differential,
                forfeit=item.forfeit,
                support=item.support,
                damagedone=item.damagedone,
                hphealed=item.hphealed,
                luck=item.luck,
                remaininghealth=item.remaininghealth
            )
    for item in freeagencyitems:
        team=historical_team.objects.filter(league=league_,seasonname = season.seasonname).get(coach1=item.coach.coach)
        maxid+=1
        historical_freeagency.objects.create(team=team,addedpokemon=item.addedpokemon,droppedpokemon=item.droppedpokemon)
        item.delete()
    for item in tradingitems:
        team=historical_team.objects.filter(league=league_,seasonname = season.seasonname).get(coach1=item.coach.coach)
        historical_trading.objects.create(team=team,addedpokemon=item.addedpokemon,droppedpokemon=item.droppedpokemon)
        item.delete()
    startid=draftitems.order_by('id').first().id
    for item in draftitems:
        team=historical_team.objects.filter(league=league_,seasonname = season.seasonname).get(coach1=item.team.coach)
        historical_draft.objects.create(team=team,pokemon=item.pokemon,picknumber=item.id-startid+1)
        item.delete()
    for item in rosteritems:
        team=historical_team.objects.filter(league=league_,seasonname = season.seasonname).get(coach1=item.team.coach)
        historical_roster.objects.create(team=team,pokemon=item.pokemon,kills=item.kills,deaths=item.deaths,differential=item.differential,gp=item.gp,gw=item.gw,support=item.support,damagedone=item.damagedone,hphealed=item.hphealed,luck=item.luck,remaininghealth=item.remaininghealth)
        item.delete()
    for item in scheduleitems:
        team1=historical_team.objects.filter(league=league_,seasonname = season.seasonname).get(coach1=item.team1.coach)
        team2=historical_team.objects.filter(league=league_,seasonname = season.seasonname).get(coach1=item.team2.coach)
        if item.team1==item.winner:
            winner=team1
        elif item.team2==item.winner:
            winner=team1
        else:
            winner=None
        histmatch=historical_match.objects.create(
            week=item.week,
            team1=team1,
            team1alternateattribution=item.team1alternateattribution,
            team2=team2,
            team2alternateattribution=item.team2alternateattribution,
            winner = winner,
            winneralternateattribution=item.winneralternateattribution,
            team1score = item.team1score,
            team2score = item.team2score,
            replay = item.replay,
            team1usedz = item.team1usedz,
            team2usedz = item.team2usedz,
            team1megaevolved = item.team1megaevolved,
            team2megaevolved = item.team2megaevolved
        )
        try: 
            mr=item.match_replay
            historical_match_replay.objects.create(match=histmatch,data=mr.data)
        except:
            pass
        item.delete()   
    coachdataitems.delete()
    season.delete()
    return redirect('leagues_hosted_settings')

@login_required
@check_if_subleague
@check_if_season
@check_if_host
def createroundrobinschedule(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    leaguesettings=seasonsetting.objects.get(subleague=subleague)
    needednumberofcoaches=leaguesettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=subleague.league)
    currentcoachescount=len(currentcoaches)
    existingmatches=schedule.objects.all().filter(season=leaguesettings).exclude(replay='Link')
    if existingmatches.count()>0:
        messages.error(request,'Matches already exist!',extra_tags='danger')
        return redirect('manage_seasons',league_name=league_name,subleague_name=subleague_name)
    schedule.objects.all().filter(season=leaguesettings).delete()
    #get conferences
    conferences=conference_name.objects.all().filter(subleague=subleague)
    conference_rosters=[]
    for c in conferences:
        coachs=coachdata.objects.all().filter(conference=c)
        conference_rosters.append(coachs)
    #create matches
    interconfteams=[]
    for conference in conference_rosters:
        conference=list(conference)
        if len(conference) % 2:
            conference.append(None)
        count=len(conference)
        sets=count-1
        interconf=[]
        for week in range(sets):
            for i in range(int(count/2)):
                if conference[i]!=None and conference[count-i-1]!=None:
                    schedule.objects.create(season=leaguesettings,week=str(week+1),team1=conference[i],team2=conference[count-i-1])
                elif conference[i]==None:
                    interconf.append(conference[count-i-1])
                elif conference[count-i-1]==None:
                    interconf.append(conference[i])
            conference.insert(1, conference.pop())
        interconfteams.append(interconf)
    for i in range(len(interconfteams[0])):
        schedule.objects.create(season=leaguesettings,week=str(i+1),team1=interconfteams[0][i],team2=interconfteams[1][i])
    return redirect('manage_seasons',league_name=league_name,subleague_name=subleague_name)

@login_required
@check_if_subleague
@check_if_season
@check_if_host
def create_match(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    seasonsettings=subleague.seasonsetting
    leaguesettings=league_settings.objects.get(league_name=subleague.league)
    currentcoaches=coachdata.objects.filter(league_name=subleague.league)
    form = CreateMatchForm(seasonsettings,subleague,initial={'season':seasonsettings})
    settingheading='Create New Match'
    edit=False
    matchid=None
    if request.method == 'POST':  
        formpurpose=request.POST['formpurpose']
        if formpurpose=="Create":
            form = CreateMatchForm(seasonsettings,subleague,request.POST)
            if form.is_valid() :
                form.save()
                messages.success(request,'That match has been added!')
            return redirect('create_match',league_name=league_name,subleague_name=subleague_name)
        elif formpurpose=="Submit":
            matchofinterest=schedule.objects.get(id=request.POST['matchid'])
            form = CreateMatchForm(seasonsettings,subleague,request.POST,instance=matchofinterest)
            if form.is_valid() :
                form.save()
                messages.success(request,'That match has been added!')
            else:
                print(form.errors)
            return redirect('create_match',league_name=league_name,subleague_name=subleague_name)
        elif formpurpose=="Edit":
            matchofinterest=schedule.objects.get(id=request.POST['matchid'])
            form = CreateMatchForm(seasonsettings,subleague,instance=matchofinterest)
            settingheading='Edit Match'
            matchid=matchofinterest.id
            edit=True
        elif formpurpose=="Delete":
            schedule.objects.get(id=request.POST['matchid']).delete()
            messages.success(request,'That match has been deleted!')
            return redirect('create_match',league_name=league_name,subleague_name=subleague_name)
    create=True
    manageseason=False
    existingmatches=schedule.objects.all().filter(season=seasonsettings).order_by('week','id')
    context = {
        'subleague':subleague,
        'league_name': league_name,
        'leagueshostedsettings': True,
        'league_teams': league_teams,
        'forms': [form],
        'seasonsettings': seasonsettings,
        'settingheading': settingheading,
        'create': create,
        'edit':edit,
        'matchid':matchid,
        'manageseason': manageseason,
        'existingmatches':existingmatches,
    }
    return render(request, 'creatematch.html',context)