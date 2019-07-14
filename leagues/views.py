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

def league_detail(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        settings=league_settings.objects.get(league_name=league_)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
        conferencelist=conference_name.objects.all().filter(league=league_).order_by('id')
        conferences=[]
        for item in conferencelist:
            divisionlist=division_name.objects.all().filter(associatedconference=item).order_by('id')
            if divisionlist.count() > 0:
                divisions=[]
                for item2 in divisionlist:
                    coachs=coachdata.objects.all().filter(division=item2)
                    divisions.append([item2,coachs])
            else: 
                coachs=coachdata.objects.all().filter(conference=item).order_by('-wins','losses','-differential','teamname')
                divisions=[[None,coachs]]
            conferences.append([item,divisions])
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        applications=league_application.objects.get(applicant=request.user)
        apply=False   
    except:
        try:
            coachdata.objects.filter(league_name=league_).get(coach=request.user)
            apply=False
        except:
            try:
                coachdata.objects.filter(league_name=league_).get(teammate=request.user)
                apply=False
            except:
                apply=True
    try:
        season=seasonsetting.objects.get(league=league_)
        timezone = pytz.timezone('UTC')
        elapsed=timezone.localize(datetime.now())-season.seasonstart
        timercurrentweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
        seasonstart=str(season.seasonstart)
    except:
        season=None
        timercurrentweek=None
        seasonstart=None
    if settings.teambased:
        parent_team_list=league_team.objects.all().filter(league=league_)
        allmatches=season.schedule.all()
        numberofweeks=season.seasonlength
        for i in range(numberofweeks):
            weekmatches=allmatches.filter(week=i+1)
            incompletematches=weekmatches.filter(replay='Link').count()
            for parent_team in parent_team_list:
                leaguematches=0
                leaguewins=0
                if i==0:
                    parent_team.wins=0;parent_team.losses=0;parent_team.ties=0;parent_team.gp=0;parent_team.gw=0;parent_team.points=0;parent_team.differential=0
                for coach in parent_team.child_teams.all():
                    try:
                        coachmatch=weekmatches.get(Q(team1=coach)|Q(team2=coach))
                        if coachmatch.replay != "Link":
                            parent_team.gp+=1
                            if coach==coachmatch.winner:
                                parent_team.gw+=1
                                parent_team.differential+=abs(coachmatch.team1score-coachmatch.team2score)
                                leaguewins+=1
                            else:
                                parent_team.differential+=0-abs(coachmatch.team1score-coachmatch.team2score)
                            leaguematches+=1
                    except:
                        nomatch=True
                if leaguematches>0 and incompletematches==0:
                    winpercent=leaguewins/leaguematches
                    if winpercent>0.5:
                        parent_team.wins+=1
                        parent_team.points+=3
                    elif winpercent<0.5:
                        parent_team.losses+=1  
                    else:
                        parent_team.ties+=1 
                        parent_team.points+=1
                parent_team.save()
        parent_teams=[]
        parent_team_list=parent_team_list.order_by('-points','-gw','-differential')
        for parent_team in parent_team_list:            
            parent_teams.append([parent_team,parent_team.child_teams.all().order_by('-wins','losses','-differential')])

        context = {
        'league': league_,
        'apply': apply,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'conference': conferences[0][0],
        'season':season,
        'timercurrentweek': timercurrentweek,
        'seasonstart':seasonstart,
        'parent_teams':parent_teams,
        'coachs':coachs,
        }
        return render(request, 'league_detail_team_based.html',context)
    else:
        context = {
        'league': league_,
        'apply': apply,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'conferences': conferences,
        'season':season,
        'timercurrentweek': timercurrentweek,
        'seasonstart':seasonstart
        }
        return render(request, 'league_detail.html',context)

@login_required
def create_league(request):
    if request.method == 'POST':
        form = CreateLeagueForm(request.POST)
        if form.is_valid():
            newleague=form.save()
            messages.success(request,f'Your league has been successfully created!')
            allpokes=all_pokemon.objects.all()
            i=pokemon_tier.objects.all().order_by('id').last().id
            for item in allpokes:
                i+=1
                pokemon_tier.objects.create(id=i,pokemon=item,league=newleague)
            return redirect('league_list')
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

def recruiting_league_list(request):
    recruitinglist=league_settings.objects.filter(is_recruiting=True).filter(is_public=True).exclude(league_name__name__contains="Test")
    if recruitinglist.count()==0:
        recruitinglist=True
    context={
        'recruitinglist': recruitinglist,
        'leagueheading': 'Recruiting Leagues',
    }
    return render(request, 'leagues.html',context)

@login_required
def leagues_hosted_settings(request):
    context = {
        'settingheading': "Select League",
        'leagueshostedsettings': True,
    }
    return render(request, 'leaguelist.html',context)

@login_required
def individual_league_settings(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_instance.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
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
    }
    return render(request, 'settings.html',context)

@login_required
def discordsettings(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_instance.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    try:
        discordinstance=discord_settings.objects.get(league=league_instance)
        form=DiscordSettingsForm(instance=discordinstance)
        if request.method=='POST':
            form=DiscordSettingsForm(request.POST,instance=discordinstance)
            if form.is_valid():
                form.save()
                messages.success(request,league_name+' has been updated!')
            else:
                messages.error(request,'Form invalid!')
            return redirect('individual_league_settings',league_name=league_name)
    except Exception as e:
        print(e)
        form=DiscordSettingsForm(initial={'league':league_instance})
        if request.method=='POST':
            form=DiscordSettingsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,league_name+' has been updated!')
            else:
                messages.error(request,'Form invalid!')
            return redirect('individual_league_settings',league_name=league_name)
    context = {
        'settingheading': f'{league_name} Discord Settings',
        'forms': [form],
        'leagueshostedsettings': True,
    }
    return render(request, 'formsettings.html',context)

@login_required
def delete_league(request,league_name):
    try:
        leaguetodelete=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in leaguetodelete.host.all():
        messages.error(request,'Only a league host may delete a league!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    leaguetodelete.delete()
    messages.success(request,league_name+' has been deleted!')
    return redirect('leagues_hosted_settings')

@login_required
def league_apply(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_list')
    try:
        applications=league_application.objects.filter(league_name=league_).get(applicant=request.user)
        messages.error(request,'You have already applied to '+league_name+"!",extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    except:
        try:
            coachdata.objects.filter(league_name=league_).get(teammate=request.user)
            messages.error(request,'You are already a coach in '+league_name+"!",extra_tags='danger')
            return redirect('league_detail',league_name=league_name)
        except:
            try:
                coachdata.objects.filter(league_name=league_).get(coach=request.user)
                messages.error(request,'You are already a coach in '+league_name+"!",extra_tags='danger')
                return redirect('league_detail',league_name=league_name)
            except:
                if league_.settings.is_recruiting == False:
                    messages.error(request,league_name+' is not currently accepting applications!',extra_tags='danger')
                    return redirect('leagues_list')
                if request.method == 'POST':
                    form = LeagueApplicationForm(request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request,'You have successfully applied to '+league_name+"!")
                        return redirect('league_detail',league_name=league_name)
                else:
                    form = LeagueApplicationForm(initial={
                        'applicant': request.user,
                        'league_name': league_
                        })
                    
                context = {
                    'league': league_,
                    'forms': [form],
                }
                return render(request, 'leagueapplication.html',context)

@login_required
def manage_coachs(request,league_name):
    league_=league.objects.get(name=league_name)
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may manage coachs!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    applicants=league_application.objects.filter(league_name=league_)
    totalapplicants=len(applicants)
    coachs=coachdata.objects.filter(league_name=league_).order_by('coach__username')
    leaguecapacity=league_.settings.number_of_teams
    numberofcoachs=leaguecapacity-len(coachs)
    spotsremaining=(numberofcoachs>0)
    context = {
        'applicants': applicants,
        'coachs': coachs,
        'league_name': league_name,
        'leagueshostedsettings': True,
        'numberofcoachs': numberofcoachs,
        'totalapplicants': totalapplicants,
        'spotsremaining': spotsremaining,
    }
    return render(request, 'managecoachs.html',context)

@login_required
def add_coach(request,league_name):
    if request.POST:
        application=league_application.objects.get(pk=request.POST['coach'])
        coachdata.objects.create(coach=application.applicant,league_name=application.league_name)
        application.delete()
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
            coachtoremove=coachdata.objects.get(pk=request.POST['coach'])
            #league_application.objects.create(applicant=coachtoremove.coach,league_name=coachtoremove.league_name)
            #coachtoremove.delete()
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

@login_required
def manage_tiers(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        form = CreateTierForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been added!')
            return redirect('manage_tiers',league_name=league_name)
    else:
        form = CreateTierForm(initial={'league': league_})

    pokemontiers=pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','tier')
    leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'managetiers': True,
    }
    return render(request, 'managetiers.html',context)

@login_required
def manage_seasons(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    leaguesettings=league_settings.objects.get(league_name=league_)
    needednumberofcoaches=leaguesettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=league_)
    currentcoachescount=len(currentcoaches)
    if needednumberofcoaches != currentcoachescount: 
        messages.error(request,'You can only utilize season settings if you have designated the same number of coaches as available spots',extra_tags='danger')
        return redirect('individual_league_settings',league_name=league_name)
    if request.method == 'POST':
        try:
            seasonsettings=seasonsetting.objects.get(league=league_)
            form = EditSeasonSettingsForm(request.POST,instance=seasonsettings)
            if form.is_valid():
                form.save()
                messages.success(request,'Season settings have been updated!')
            else:
                messages.error(request,form.errors,extra_tags='danger')    
            return redirect('manage_seasons',league_name=league_name)
        except:    
            form = CreateSeasonSettingsForm(request.POST)
            if form.is_valid() :
                thisseason=form.save()
                picksperteam=form.cleaned_data['picksperteam']
                rosterid=roster.objects.all().order_by('id').last().id
                for coach in currentcoaches:
                    for i in range(picksperteam):
                        rosterid+=1
                        roster.objects.create(id=rosterid,season=thisseason,team=coach)
                rule.objects.create(season=thisseason)
                messages.success(request,'Your season has been created!')
                return redirect('manage_seasons',league_name=league_name)
    else:
        try:
            seasonsettings=seasonsetting.objects.get(league=league_)
            form = EditSeasonSettingsForm(instance=seasonsettings)
            settingheading='Update Season Settings'
            create=False
            manageseason=True
        except:
            seasonsettings=None
            form = CreateSeasonSettingsForm(initial={'league': league_})
            settingheading='Create New Season'
            create=True
            manageseason=False
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'forms': [form],
        'seasonsettings': seasonsettings,
        'settingheading': settingheading,
        'create': create,
        'manageseason': manageseason,    
    }
    return render(request, 'settings.html',context)

@login_required
def delete_tier(request,league_name):
    if request.POST:
        tiertodelete=leaguetiers.objects.get(pk=request.POST['tiertodelete'])
        tiertodelete.delete()
    return redirect('manage_tiers',league_name=league_name)

@login_required
def edit_tier(request,league_name,tierid):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        tierinstance=leaguetiers.objects.get(pk=tierid)
        form = UpdateTierForm(request.POST,instance=tierinstance)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been edited!')
            return redirect('manage_tiers',league_name=league_name)
    else:
        tierinstance=leaguetiers.objects.get(pk=tierid)
        form=UpdateTierForm(instance=tierinstance)
    pokemontiers=None#pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','points')
    leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'editingtier': True,
    }
    return render(request, 'managetiers.html',context)

@login_required
def update_tier(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.POST:
        pokemonofinterest=all_pokemon.objects.get(pokemon=request.POST['pokemon-select'])
        pokemontoupdate=pokemon_tier.objects.filter(league=league_).get(pokemon=pokemonofinterest)
        tiertoadd=leaguetiers.objects.get(pk=request.POST['tier-select'])
        pokemontoupdate.tier=tiertoadd
        pokemontoupdate.save()
        messages.success(request,'Tier has been edited!')
    return redirect('manage_tiers',league_name=league_name)

@login_required
def view_tier(request,league_name,tier):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        form = CreateTierForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been added!')
            return redirect('manage_tiers',league_name=league_name)
    else:
        form = CreateTierForm(initial={'league': league_})
        pokemontiers=pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','tier')
        leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
        if tier=="Untiered":
            pokemonlist=pokemon_tier.objects.filter(league=league_,tier=None).all().order_by('pokemon__pokemon')
        else:
            tier=tier.replace("_"," ")
            tierofinterest=leaguetiers.objects.filter(league=league_,tiername=tier).first()
            pokemonlist=pokemon_tier.objects.filter(league=league_,tier=tierofinterest).all().order_by('pokemon__pokemon')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'pokemonlist': pokemonlist
    }
    return render(request, 'managetiers.html',context)

@login_required
def default_tiers(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        tier="Untiered"
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        purpose=request.POST['purposeid']
        if purpose=='Select':
            templatetierset=leaguetiertemplate.objects.all().filter(template=request.POST['template-select'])
            templatepokemonset=pokemon_tier_template.objects.all().filter(template=request.POST['template-select'])
            existingtiers=leaguetiers.objects.all().filter(league=league_)
            existingpokemontiers=pokemon_tier.objects.all().filter(league=league_)
            for item in existingtiers:
                item.delete()
            for item in templatetierset:
                leaguetiers.objects.create(league=league_,tiername=item.tiername,tierpoints=item.tierpoints)
            for item in existingpokemontiers:
                item.delete()
            i=pokemon_tier.objects.all().order_by('id').last().id
            for item in templatepokemonset:
                i+=1
                tiertouse=leaguetiers.objects.filter(league=league_).get(tiername=item.tier.tiername)
                pokemon_tier.objects.create(id=i,pokemon=item.pokemon,league=league_,tier=tiertouse)
            messages.success(request,'The template has been applied!')
        elif purpose=="Use":
            #delete existing
            league_.leaguetiers.all().delete()
            league_.leaguepokemontiers.all().delete()
            #add new
            leagueofinterest=league.objects.get(id=request.POST['leagueid'])
            leagueofinteresttiers=leagueofinterest.leaguetiers.all()
            for item in leagueofinteresttiers:
                leaguetiers.objects.create(league=league_,tiername=item.tiername,tierpoints=item.tierpoints)
            leagueofinteresttiering=leagueofinterest.leaguepokemontiers.all()
            startid=pokemon_tier.objects.all().order_by('id').last().id
            for item in leagueofinteresttiering:
                startid+=1
                tiertouse=leaguetiers.objects.filter(league=league_).get(tiername=item.tier.tiername)
                pokemon_tier.objects.create(id=startid,pokemon=item.pokemon,league=league_,tier=tiertouse)
        return redirect('manage_tiers',league_name=league_name)
    else:
        pokemonlist=pokemon_tier.objects.filter(league=league_,tier=None).all().order_by('pokemon__pokemon')
        pokemontiers=pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','tier')
        leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
        availabletemplates=leaguetiertemplate.objects.all().distinct('template')
        form = CreateTierForm(initial={'league': league_})
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'pokemonlist': pokemonlist,
        'defaulttemplate': True,
        'availabletemplates': availabletemplates,
    }
    return render(request, 'managetiers.html',context)

@login_required
def set_draft_order(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    leaguesettings=league_settings.objects.get(league_name=league_)
    needednumberofcoaches=leaguesettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=league_).order_by('teamname')
    currentcoachescount=len(currentcoaches)
    try:
        seasonsettings=seasonsetting.objects.get(league=league_)
        draftstyle=seasonsettings.drafttype  
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('individual_league_settings',league_name=league_name)
    if needednumberofcoaches != currentcoachescount: 
        messages.error(request,'You can only utilize season settings if you have designated the same number of coaches as available spots',extra_tags='danger')
        return redirect('individual_league_settings',league_name=league_name)
    if request.method == 'POST':
        currentdraft=draft.objects.all().filter(season=seasonsettings)
        for item in currentdraft:
            item.delete()
        if draftstyle=="Snake":
            order=[]
            for i in range(needednumberofcoaches):
                order.append(coachdata.objects.filter(teamname=request.POST[str(i+1)],league_name=league_).first())
            flippedorder=order[::-1]
            numberofpicks=seasonsettings.picksperteam
            for i in range(numberofpicks):
                if i%2 == 0:
                    for item in order:
                        draft.objects.create(season=seasonsettings,team=item)
                else:    
                    for item in flippedorder:
                        draft.objects.create(season=seasonsettings,team=item)
        messages.success(request,'Draft order has been set!')
        return redirect('individual_league_settings',league_name=league_name)        
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'settingheading': 'Set Draft Order',
        'currentcoaches': currentcoaches,
    }
    return render(request, 'draftorder.html',context)

@login_required
def add_conference_and_division_names(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        leaguesettings=league_settings.objects.get(league_name=league_)
        currentconferences = conference_name.objects.all().filter(league=league_)
        currentdivisions = division_name.objects.all().filter(league=league_)
        totalconferences=leaguesettings.number_of_conferences
        totaldivisions=leaguesettings.number_of_divisions
        neededconferences=totalconferences-currentconferences.count()
        neededdivisions=totaldivisions-currentdivisions.count()
        if int(totalconferences/totaldivisions)==1:
            neededdivisions=0 
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        name=request.POST['itemname']
        category=request.POST['category']
        if category=='conference':
            conference_name.objects.create(league=league_,name=name)
        elif category=='division':
            associatedconference=conference_name.objects.all().filter(league=league_).get(name=request.POST['divisionconference'])
            division_name.objects.create(league=league_,name=name,associatedconference=associatedconference)
        messages.success(request,f'{name} has been added as a {category}!')
        return redirect('add_conference_and_division_names',league_name=league_name)        
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'currentconferences': currentconferences,
        'currentdivisions': currentdivisions,
        'neededconferences': neededconferences,
        'neededdivisions': neededdivisions,
    }
    return render(request, 'addconferencesanddivisions.html',context)

@login_required
def delete_conference(request,league_name):
    if request.method=="POST":
        itemid=request.POST['itemid']
        itemtodelete=conference_name.objects.get(pk=itemid)
        itemtodelete.delete()
        messages.success(request,'Conference has been deleted!')
    return redirect('add_conference_and_division_names',league_name=league_name)        

@login_required
def delete_division(request,league_name):
    if request.method=="POST":
        itemid=request.POST['itemid']
        itemtodelete=division_name.objects.get(pk=itemid)
        itemtodelete.delete()
        messages.success(request,'Division has been deleted!')
    return redirect('add_conference_and_division_names',league_name=league_name)        

@login_required
def manage_coach(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user not in league_.host.all():
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
    }
    if request.method == 'POST':
        formtype=request.POST['formtype']
        coach=coachdata.objects.get(id=request.POST['coach'])
        if formtype=="load":
            form=ManageCoachForm(league_,instance=coach)
            try:
                season=seasonsetting.objects.get(league=league_)
                seasonnotinsession=False
            except:
                seasonnotinsession=True
            context.update({
                'coach':coach,
                'form':form,
                'coachform':True,
                'seasonnotinsession': seasonnotinsession,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="update":
            form=ManageCoachForm(league_,request.POST,request.FILES,instance=coach)
            if form.is_valid():
                #form.save()
                print('here')
                messages.success(request,f'{coach.coach} has been updated!')
                return redirect('manage_coachs', league_name=league_name)
        elif formtype=="Adjust Draft":
            context.update({
                'coach':coach,
                'adjustdraft': True,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="Adjust Roster":
            context.update({
                'coach':coach,
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
                'form': UpdateCoachRecordForm(instance=coach),
                'coach':coach,
                'adjustrecord': True,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="updatecoachdata":
            form=UpdateCoachRecordForm(request.POST,instance=coach)
            if form.is_valid():
                form.save()
                messages.success(request,f'{coach.coach} has been updated!')
                return redirect('manage_coachs', league_name=league_name)
            return redirect('manage_coachs', league_name=league_name)
        elif formtype=="Add Showdown Alt":
            alts=showdownalts.objects.all().filter(user=coach.coach)
            context.update({
                'alts':alts,
                'coach':coach,
                'addalt': True,
                })
            return render(request, 'managecoach.html',context)
        elif formtype=="addalt":
            showdownalts.objects.create(user=coach.coach,showdownalt=request.POST['givenalt'])
            messages.success(request,f'{coach.coach} has been updated!')
            return redirect('manage_coachs', league_name=league_name)
    return redirect('manage_coachs', league_name=league_name)

@login_required
def designate_z_users(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
        coachinstance=coachdata.objects.filter(league_name=league_instance).filter(Q(coach=request.user)|Q(teammate=request.user)).first()
        settings=league_settings.objects.get(league_name=league_instance)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_coaching_settings')
    try:
        season=seasonsetting.objects.get(league=league_instance)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('leagues_coaching_settings')
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
        season=seasonsetting.objects.get(league=league_instance)
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