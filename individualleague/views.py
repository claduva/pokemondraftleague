from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

import math
from datetime import datetime, timezone, timedelta
import pytz
from dal import autocomplete

from .models import *
from leagues.models import *
from pokemondatabase.models import *
from accounts.models import *
from .forms import *
from pokemondraftleague.customdecorators import check_if_subleague, check_if_league, check_if_season, check_if_team, check_if_host

@check_if_league
def league_detail(request,league_name):
    league_=league.objects.get(name=league_name)
    subleagues=league_.subleague.all()
    if subleagues.count()==1:
        loi=subleagues.first()
        return redirect('subleague_detail',league_name=league_name,subleague_name=loi.subleague)
    else:
        loi=subleagues.first()
        return redirect('subleague_detail',league_name=league_name,subleague_name=loi.subleague)

@check_if_subleague
def subleague_detail(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    settings=league_settings.objects.get(league_name=subleague.league)
    conferencelist=conference_name.objects.all().filter(league=subleague.league).order_by('id')
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
    try:
        applications=league_application.objects.get(applicant=request.user)
        apply=False   
    except:
        try:
            coachdata.objects.filter(league_name=subleague.league).get(coach=request.user)
            apply=False
        except:
            try:
                coachdata.objects.filter(league_name=subleague.league).get(teammate=request.user)
                apply=False
            except:
                apply=True
    try:
        season=seasonsetting.objects.get(league=subleague.league)
        timezone = pytz.timezone('UTC')
        elapsed=timezone.localize(datetime.now())-season.seasonstart
        timercurrentweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
        seasonstart=str(season.seasonstart)
    except:
        season=None
        timercurrentweek=None
        seasonstart=None
    if settings.teambased:
        parent_team_list=league_team.objects.all().filter(league=subleague.league)
        try:
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
        except:
            pass
        parent_teams=[]
        parent_team_list=parent_team_list.order_by('-points','-gw','-differential')
        for parent_team in parent_team_list:            
            parent_teams.append([parent_team,parent_team.child_teams.all().order_by('-wins','losses','-differential')])
        context = {
        'subleague': subleague,
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
        'subleague': subleague,
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

@check_if_subleague
@check_if_season
@check_if_team
def team_page(request,league_name,subleague_name,team_abbreviation):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    team=league_teams.get(teamabbreviation=team_abbreviation)
    teamroster=team.teamroster.all().order_by('id')
    matchs=schedule.objects.all().filter(season=season).filter(Q(team1=team)|Q(team2=team))
    results=matchs.exclude(replay="Link").order_by('-id')
    upcoming=matchs.filter(replay="Link").order_by('id')[0:4]
    context = {
        'subleague':subleague,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'team': team,
        'roster': teamroster,
        'results':results,
        'upcoming': upcoming
    }
    return render(request, 'teampage.html',context)

@check_if_subleague
@check_if_season
def league_draft(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    coachcount=league_teams.count()
    season=subleague.seasonsetting
    draftstart=str(season.draftstart)
    drafttimer=season.drafttimer   
    draftlist=draft.objects.all().filter(season=season).order_by('id') 
    draftsize=draftlist.count()
    picksremaining=draftlist.filter(pokemon__isnull=True).count()
    if draftsize>0:
        draftprogress=int(math.floor((draftsize-picksremaining)/draftsize*100))
    else:
        draftprogress=0
    is_host=(request.user in subleague.league.host.all())
    currentpick=draftlist.filter(pokemon__isnull=True,skipped=False).first()
    canskippick=False
    try:
        currentpickdraft=draftlist.filter(team=currentpick.team,pokemon__isnull=False)
        if currentpickdraft.count()>=8 and (request.user==currentpick.team.coach or request.user==currentpick.team.teammate): 
            canskippick=True
    except:
        pass
    if picksremaining>0:
    ## go through left picks
        try:
            picksleft=left_pick.objects.filter(coach=currentpick.team).order_by('id')
        except:
            picksleft=left_pick.objects.none()
        if picksleft.count()>0:
            for item in picksleft:
                #check pick
                searchroster=roster.objects.filter(season=season,pokemon=item.pick).first()
                if searchroster == None:
                    currentpick.pokemon=item.pick
                    rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
                    rosterspot.pokemon=item.pick
                    rosterspot.save()
                    currentpick.save()
                    item.delete()
                    text=f'The {currentpick.team.teamname} have drafted {item.pick.pokemon}'
                    draftchannel=subleague.league.discord_settings.draftchannel
                    #send to bot
                    try:
                        upnext=draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.username
                        upnextid=str(draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.profile.discordid)
                    except:
                        upnext="The draft has concluded"
                    draft_announcements.objects.create(
                        league=subleague.league.discord_settings.discordserver,
                        league_name=subleague.league.name.replace(' ','%20'),
                        text=text,
                        upnext=upnext,
                        draftchannel=draftchannel,
                        upnextid=upnextid
                    )
                    return redirect('league_draft',league_name=league_name)
                else:
                    searchroster=roster.objects.filter(season=season,pokemon=item.backup).first()     
                    if searchroster == None:
                        currentpick.pokemon=item.backup
                        rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
                        rosterspot.pokemon=item.backup
                        rosterspot.save()
                        currentpick.save()
                        item.delete()
                        text=f'The {currentpick.team.teamname} have drafted {item.backup.pokemon}'
                        draftchannel=subleague.league.discord_settings.draftchannel
                        #send to bot
                        try:
                            upnext=draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.username
                            upnextid=str(draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.profile.discordid)
                        except:
                            upnext="The draft has concluded"
                        draft_announcements.objects.create(
                            league=subleague.league.discord_settings.discordserver,
                            league_name=subleague.league.name.replace(' ','%20'),
                            text=text,
                            upnext=upnext,
                            draftchannel=draftchannel,
                            upnextid=upnextid
                        )
                        return redirect('league_draft',league_name=league_name)
                    else:     
                        item.delete()
    ##
    candraft=False
    if picksremaining >0:
        try:
            if currentpick.team.coach == request.user or currentpick.team.teammate == request.user:
                candraft=True
        except:
            candraft=False
    if currentpick==None:
        draftactive=False
        availablepoints=0
    else:
        draftactive=True
        draftersroster=roster.objects.all().filter(season=season,team=currentpick.team)
        pointsused=0
        for item in draftersroster:
            tier=pokemon_tier.objects.filter(league=subleague.league,pokemon=item.pokemon).first()
            if tier != None:    
                pointsused+=tier.tier.tierpoints
        budget=season.draftbudget
        availablepoints=budget-pointsused
    if picksremaining==draftsize:
        pickend=str(season.draftstart+timedelta(hours=12))
    else:  
        if picksremaining>0:
            try:
                pickend=str(draftlist.get(id=currentpick.id-1).picktime+timedelta(hours=12))
            except:
                pickend = None
        else: 
            pickend = None
    if request.method == "POST":
        if request.POST['purpose']=="Submit":
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
            rosterspot.save()
            currentpick.save()
            text=f'The {currentpick.team.teamname} have drafted {draftpick.pokemon}'
            draftchannel=subleague.league.discord_settings.draftchannel
            #send to bot
            try:
                upnext=draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.username
                upnextid=str(draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.profile.discordid)
            except:
                upnext="The draft has concluded"
            draft_announcements.objects.create(
                league=subleague.league.discord_settings.discordserver,
                league_name=subleague.league.name.replace(' ','%20'),
                text=text,
                upnext=upnext,
                draftchannel=draftchannel,
                upnextid=upnextid
            )
            messages.success(request,'Your draft pick has been saved!')
        elif request.POST['purpose']=="Leave":
            pokemonlist=all_pokemon.objects.all()
            form=LeavePickForm(pokemonlist,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Your pick has been left!')
            print("Leave Pick")
        elif request.POST['purpose']=="Delete":
            left_pick.objects.get(id=request.POST['pickid']).delete()
            messages.success(request,'Your pick was deleted!')
        elif request.POST['purpose']=="Skip":
            currentpick.skipped=True
            currentpick.save()
            messages.success(request,'That draft pick has been skipped!')
        elif request.POST['purpose']=="Mark Draft as Done":
            currentpick.skipped=True
            currentpick.save()
            otherpicks=draftlist.filter(team=currentpick.team,pokemon__isnull=True,skipped=False)
            for p in otherpicks:
                p.skipped=True
                p.save()
            messages.success(request,'That draft pick has been skipped!')
        return redirect('league_draft',league_name=league_name)
    bannedpokemon=pokemon_tier.objects.all().filter(league=subleague.league).filter(tier__tiername='Banned').values_list('pokemon',flat=True)
    takenpokemon=roster.objects.all().filter(season=season).exclude(pokemon__isnull=True).values_list('pokemon',flat=True)
    availablepokemon=all_pokemon.objects.all().order_by('pokemon').exclude(id__in=takenpokemon).exclude(id__in=bannedpokemon)
    try:
        usercoach=coachdata.objects.filter(Q(coach=request.user)|Q(teammate=request.user)).get(league_name=subleague.league)
        leftpicks=left_pick.objects.all().filter(season=season,coach=usercoach)
        form=LeavePickForm(availablepokemon,initial={'season':season,'coach':usercoach})
    except:
        form=None
        leftpicks=None
    draftorder_=draftlist[0:coachcount]
    draftorder=[]
    for item in draftorder_:
        budget=season.draftbudget
        team_=item.team.draftpicks.all()
        team=[]
        for pick in team_:
            if pick.pokemon != None:
                cost=pick.pokemon.pokemon_tiers.all().get(league=subleague.league).tier.tierpoints
                team.append([pick,cost])
                budget+=(-cost)
            else:
                team.append([pick,'-'])
        pointsused=season.draftbudget-budget
        draftorder.append([item,budget,pointsused,team])
    context = {
        'subleague':subleague,
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
        'draftorder':draftorder,
        'candraft':candraft,
        'form':form,
        'leftpicks': leftpicks,
        'canskippick':canskippick,
    }
    return render(request, 'draft.html',context)

@login_required
@check_if_subleague
@check_if_season
@check_if_host
def create_match(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    seasonsettings=subleague.seasonsetting
    leaguesettings=league_settings.objects.get(league_name=subleague.league)
    needednumberofcoaches=leaguesettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=subleague.league)
    currentcoachescount=len(currentcoaches)
    if needednumberofcoaches != currentcoachescount: 
        messages.error(request,'You can only utilize season settings if you have designated the same number of coaches as available spots',extra_tags='danger')
        return redirect('individual_league_settings',league_name=league_name)
    form = CreateMatchForm(seasonsettings,subleague.league,initial={'season':seasonsettings})
    settingheading='Create New Match'
    edit=False
    matchid=None
    if request.method == 'POST':  
        formpurpose=request.POST['formpurpose']
        if formpurpose=="Create":
            form = CreateMatchForm(seasonsettings,subleague.league,request.POST)
            if form.is_valid() :
                form.save()
                messages.success(request,'That match has been added!')
            return redirect('create_match',league_name=league_name)
        elif formpurpose=="Submit":
            matchofinterest=schedule.objects.get(id=request.POST['matchid'])
            form = CreateMatchForm(seasonsettings,subleague.league,request.POST,instance=matchofinterest)
            if form.is_valid() :
                form.save()
                messages.success(request,'That match has been added!')
            else:
                print(form.errors)
            return redirect('create_match',league_name=league_name)
        elif formpurpose=="Edit":
            matchofinterest=schedule.objects.get(id=request.POST['matchid'])
            form = CreateMatchForm(seasonsettings,league_,instance=matchofinterest)
            settingheading='Edit Match'
            matchid=matchofinterest.id
            edit=True
        elif formpurpose=="Delete":
            schedule.objects.get(id=request.POST['matchid']).delete()
            messages.success(request,'That match has been deleted!')
            return redirect('create_match',league_name=league_name)
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
    return render(request, 'settings.html',context)

@check_if_subleague
@check_if_season
def league_schedule(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    coachcount=league_teams.count()
    season=subleague.seasonsetting
    leagueschedule=[]
    numberofweeks=season.seasonlength
    for i in range(numberofweeks):
        matches_=schedule.objects.all().filter(week=str(i+1),season=season).order_by('id')
        matches=[]
        for item in matches_:
            pickemlist=pickems.objects.all().filter(match=item)
            try:
                userpickem=pickemlist.get(user=request.user)
            except:
                userpickem=None
            team1count=pickemlist.filter(pick=item.team1).count()
            team2count=pickemlist.filter(pick=item.team2).count()
            pickem={
                'team1count':team1count,
                'team2count':team2count,
                'userpickem':userpickem,
            }
            matches.append([item,pickem])
        leagueschedule.append([str(i+1),matches])
    ishost=(request.user==subleague.league.host)
    timezone = pytz.timezone('UTC')
    elapsed=timezone.localize(datetime.now())-season.seasonstart
    currentweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'leagueschedule': leagueschedule,
        'ishost': ishost,
        'numberofweeks': range(numberofweeks),
        'currentweek': currentweek,
    }
    if request.method=="POST":
        if request.POST['purpose']=="Go":
            weekselect=request.POST['weekselect']
            if weekselect=="All":
                donothing=True
            else:
                matches_=schedule.objects.all().filter(week=weekselect,season=season).order_by('id')
                matches=[]
                for item in matches_:
                    pickemlist=pickems.objects.all().filter(match=item)
                    try:
                        userpickem=pickemlist.get(user=request.user)
                    except:
                        userpickem=None
                    team1count=pickemlist.filter(pick=item.team1).count()
                    team2count=pickemlist.filter(pick=item.team2).count()
                    pickem={
                        'team1count':team1count,
                        'team2count':team2count,
                        'userpickem':userpickem,
                    }
                    matches.append([item,pickem])
                leagueschedule=[[weekselect,matches]]
                context.update({'leagueschedule':leagueschedule})
                return render(request, 'schedule.html',context)
        elif request.POST['purpose']=="t1pickem":
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            try:
                pickemtoupdate=pickems.objects.all().filter(match=matchtoupdate).get(user=request.user)
                if pickemtoupdate.pick==matchtoupdate.team1:
                    pickemtoupdate.delete()
                else:
                    pickemtoupdate.pick=matchtoupdate.team1
                    pickemtoupdate.save()
            except:
                pickem=pickems.objects.create(user=request.user,match=matchtoupdate,pick=matchtoupdate.team1)
            return redirect('league_schedule',league_name=league_name)
        elif request.POST['purpose']=="t2pickem":
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            try:
                pickemtoupdate=pickems.objects.all().filter(match=matchtoupdate).get(user=request.user)
                if pickemtoupdate.pick==matchtoupdate.team2:
                    pickemtoupdate.delete()
                else:
                    pickemtoupdate.pick=matchtoupdate.team2
                    pickemtoupdate.save()
            except:
                pickem=pickems.objects.create(user=request.user,match=matchtoupdate,pick=matchtoupdate.team2)
            return redirect('league_schedule',league_name=league_name)
        else:
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            team1=matchtoupdate.team1
            team2=matchtoupdate.team2
            if request.POST['purpose']=="t1ff":
                matchtoupdate.replay=f'{team1.teamabbreviation} Forfeits'
                team1.losses+=1; team2.wins+=1
                team1.differential+=(-6); team2.differential+=3
                team1.forfeit+=1
                if team1.streak>-1:
                    team1.streak=-1
                else:
                    team1.streak+=(-1)
                if team2.streak>-1:
                    team2.streak+=1
                else:
                    team2.streak=1
                messages.success(request,'Match has been forfeited by Team 1!')
            elif request.POST['purpose']=="t2ff":
                matchtoupdate.replay=f'{team2.teamabbreviation} Forfeits'
                team1.wins+=1; team2.losses+=1
                team1.differential+=3; team2.differential+=(-6)
                team2.forfeit+=1
                if team1.streak>-1:
                    team1.streak+=1
                else:
                    team1.streak=1
                if team2.streak>-1:
                    team2.streak=-1
                else:
                    team2.streak+=(-1)
                messages.success(request,'Match has been forfeited by Team 2!')
            elif request.POST['purpose']=="bothff":
                matchtoupdate.replay='Both Teams Forfeit'
                team1.losses+=1; team2.losses+=1
                team1.differential+=(-6); team2.differential+=(-6)
                team1.forfeit+=1; team2.forfeit+=1
                if team1.streak>-1:
                    team1.streak=-1
                else:
                    team1.streak+=(-1)
                if team2.streak>-1:
                    team2.streak=-1
                else:
                    team2.streak+=(-1)
                messages.success(request,'Match has been forfeited by both teams!')
            team1.save()
            team2.save()
            matchtoupdate.save()
            league_=matchtoupdate.season.league
            discordserver=league_.discord_settings.discordserver
            discordchannel=league_.discord_settings.replaychannel
            title=f"Week: {matchtoupdate.week}. {matchtoupdate.team1.teamname} vs {matchtoupdate.team2.teamname}: {matchtoupdate.replay}."
            replay_announcements.objects.create(
                league = discordserver,
                league_name = league_.name,
                text = title,
                replaychannel = discordchannel
            )
            return redirect('league_schedule',league_name=league_name)
    return render(request, 'schedule.html',context)

@check_if_subleague
@check_if_season
def league_matchup(request,league_name,subleague_name,matchid):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    try:
        match=schedule.objects.get(id=matchid)
    except:
        messages.error(request,'Match does not exist!',extra_tags='danger')
        return redirect('league_schedule',league_name=league_name)
    team1roster_=roster.objects.filter(season=season,team=match.team1,pokemon__isnull=False).order_by('pokemon__pokemon')
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

    team2roster_=roster.objects.filter(season=season,team=match.team2,pokemon__isnull=False).order_by('pokemon__pokemon')
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
        'subleague': subleague,
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

@check_if_subleague
@check_if_season
def league_rules(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    ruleset=rule.objects.get(season=season)
    is_host=(request.user in subleague.league.host.all())
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'ruleset': ruleset,
        'is_host': is_host,
    }
    return render(request, 'rules.html',context)

@check_if_subleague
@check_if_season
@check_if_host
def edit_league_rules(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    ruleset=rule.objects.get(season=season)
    if request.method=="POST":
        form=RuleChangeForm(request.POST,instance=ruleset)
        if form.is_valid():
            form.save()
            messages.success(request,'Rules have been updated!')
        return redirect('league_rules',league_name=league_name)
    form=RuleChangeForm(instance=ruleset)
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'ruleset': ruleset,
        'is_host': True,
        'editrules': True,
        'form': form,
    }
    return render(request, 'rules.html',context)

@check_if_subleague
def league_tiers(request,league_name,subleague_name):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    tierlist_=pokemon_tier.objects.all().filter(league=subleague.league).exclude(tier__tiername="Banned").order_by('-tier__tierpoints','pokemon__pokemon')
    tierchoices=leaguetiers.objects.all().filter(league=subleague.league).exclude(tiername="Banned").order_by('tiername')
    rosterlist=roster.objects.all().filter(season__league=subleague.league)
    rosterlist_=list(rosterlist.values_list('pokemon',flat=True))
    tierlist=[]
    for item in tierlist_:
        if item.pokemon.id in rosterlist_:
            owner=rosterlist.get(pokemon__id=item.pokemon.id)
            tierlist.append((item,f"Signed by {owner.team.teamabbreviation}"))
        else:
            tierlist.append((item,"FREE"))
    types=pokemon_type.objects.all().distinct('typing').values_list('typing',flat=True)
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'tiers': tierlist,
        'types':types,
        'tierchoices':tierchoices,
    }
    return render(request, 'tiers.html',context)

@login_required
@check_if_subleague
@check_if_season
def freeagency(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    coach=coachdata.objects.all().filter(league_name=subleague.league).filter(Q(coach=request.user)|Q(teammate=request.user)).first()
    coachrosterids=coach.teamroster.all().order_by('pokemon__pokemon').exclude(pokemon__isnull=True).values_list('pokemon',flat=True)
    coachroster=all_pokemon.objects.all().order_by('pokemon').filter(id__in=coachrosterids)
    bannedpokemon=pokemon_tier.objects.all().filter(league=subleague.league).filter(tier__tiername='Banned').values_list('pokemon',flat=True)
    takenpokemon=roster.objects.all().filter(season=season).exclude(pokemon__isnull=True).values_list('pokemon',flat=True)
    availablepokemon=all_pokemon.objects.all().order_by('pokemon').exclude(id__in=takenpokemon).exclude(id__in=bannedpokemon)
    if request.method=="POST":
        form=FreeAgencyForm(coachroster,availablepokemon,request.POST)
        if form.is_valid(): 
            fadata=form.save()
            messages.success(request,f'You free agency request has been added to the queue and will be implemented following completion of this week\'s match!')
            discordserver=subleague.league.discord_settings.discordserver
            discordchannel=subleague.league.discord_settings.freeagencychannel
            request_league=seasonsetting.objects.get(league=subleague.league)
            league_start=request_league.seasonstart
            elapsed=fadata.timeadded-league_start
            weekrequested=math.ceil(elapsed.total_seconds()/60/60/24/7)
            if weekrequested>0:
                weekeffective=weekrequested+1
            else:
                weekeffective=1
            title=f"The {fadata.coach.teamname} have used a free agency to drop {fadata.droppedpokemon.pokemon} for {fadata.addedpokemon.pokemon}. Effective Week {weekeffective}."
            freeagency_announcements.objects.create(
                league = discordserver,
                league_name = subleague.league.name,
                text = title,
                freeagencychannel = discordchannel
            )
            return redirect('free_agency',league_name=league_name)
    form=FreeAgencyForm(coachroster,availablepokemon,initial={'coach':coach,'season':season})
    fa_remaining=season.freeagenciesallowed-free_agency.objects.all().filter(season=season,coach=coach).count()
    if fa_remaining < 1:
        form=None
    pendingfreeagency=free_agency.objects.all().filter(executed=False,season=season)
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'form':form,
        'fa_remaining':fa_remaining,
        'pendingfreeagency':pendingfreeagency,
    }
    return render(request, 'freeagency.html',context)

@check_if_subleague
@check_if_season
def league_leaders(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    season=subleague.seasonsetting
    leagueleaders=roster.objects.all().filter(season=season,gp__gt=0).order_by('-kills','-differential')
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'leagueleaders': leagueleaders,
    }
    return render(request, 'leagueleaders.html',context)

@login_required
@check_if_subleague
@check_if_season
def trading_view(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    coach=coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user)).first()
    coachroster=roster.objects.all().filter(season=season,team=coach,pokemon__isnull=False).order_by('pokemon__pokemon')
    availablepokemon=roster.objects.all().filter(season=season,pokemon__isnull=False).exclude(team=coach).order_by('pokemon__pokemon')
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
        form=None
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'form':form,
        'trade_remaining':trade_remaining,
    }
    return render(request, 'trading.html',context)

@check_if_subleague
@check_if_season
def league_hall_of_fame(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    is_host=(request.user in subleague.league.host.all())
    halloffameentries=None
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'is_host': is_host,
        'halloffameentries':halloffameentries,
    }
    return render(request, 'halloffame.html',context)

@check_if_subleague
@check_if_season
def league_playoffs(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    leagueschedule=[]
    playoffweeks=schedule.objects.all().filter(season=season,week__icontains='Playoffs').distinct('week')
    for item_ in playoffweeks:
        matches_=schedule.objects.all().filter(season=season,week=item_.week)
        matches=[]
        for item in matches_:
            pickemlist=pickems.objects.all().filter(match=item)
            try:
                userpickem=pickemlist.get(user=request.user)
            except:
                userpickem=None
            team1count=pickemlist.filter(pick=item.team1).count()
            team2count=pickemlist.filter(pick=item.team2).count()
            pickem={
                'team1count':team1count,
                'team2count':team2count,
                'userpickem':userpickem,
            }
            matches.append([item,pickem])
        leagueschedule.append([item_.week,matches])
    ishost=(request.user in subleague.league.host.all())
    if request.method=="POST":
        if request.POST['purpose']=="Go":
            weekselect=request.POST['weekselect']
            if weekselect=="All":
                donothing=True
            else:
                matches_=schedule.objects.all().filter(week=weekselect,season=season).order_by('id')
                matches=[]
                for item in matches_:
                    pickemlist=pickems.objects.all().filter(match=item)
                    try:
                        userpickem=pickemlist.get(user=request.user)
                    except:
                        userpickem=None
                    team1count=pickemlist.filter(pick=item.team1).count()
                    team2count=pickemlist.filter(pick=item.team2).count()
                    pickem={
                        'team1count':team1count,
                        'team2count':team2count,
                        'userpickem':userpickem,
                    }
                    matches.append([item,pickem])
                leagueschedule=[[weekselect,matches]]
        elif request.POST['purpose']=="t1pickem":
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            try:
                pickemtoupdate=pickems.objects.all().filter(match=matchtoupdate).get(user=request.user)
                if pickemtoupdate.pick==matchtoupdate.team1:
                    pickemtoupdate.delete()
                else:
                    pickemtoupdate.pick=matchtoupdate.team1
                    pickemtoupdate.save()
            except:
                pickem=pickems.objects.create(user=request.user,match=matchtoupdate,pick=matchtoupdate.team1)
            return redirect('league_playoffs',league_name=league_name)
        elif request.POST['purpose']=="t2pickem":
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            try:
                pickemtoupdate=pickems.objects.all().filter(match=matchtoupdate).get(user=request.user)
                if pickemtoupdate.pick==matchtoupdate.team2:
                    pickemtoupdate.delete()
                else:
                    pickemtoupdate.pick=matchtoupdate.team2
                    pickemtoupdate.save()
            except:
                pickem=pickems.objects.create(user=request.user,match=matchtoupdate,pick=matchtoupdate.team2)
            return redirect('league_playoffs',league_name=league_name)
        else:
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            team1=matchtoupdate.team1
            team2=matchtoupdate.team2
            if request.POST['purpose']=="t1ff":
                matchtoupdate.replay='Forfeit'
                team1.losses+=1; team2.wins+=1
                team1.differential+=(-6); team2.differential+=3
                team1.forfeit+=1
                if team1.streak>-1:
                    team1.streak=-1
                else:
                    team1.streak+=(-1)
                if team2.streak>-1:
                    team2.streak+=1
                else:
                    team2.streak=1
                messages.success(request,'Match has been forfeited by Team 1!')
            if request.POST['purpose']=="t2ff":
                matchtoupdate.replay='Forfeit'
                team1.wins+=1; team2.losses+=1
                team1.differential+=3; team2.differential+=(-6)
                team2.forfeit+=1
                if team1.streak>-1:
                    team1.streak+=1
                else:
                    team1.streak=1
                if team2.streak>-1:
                    team2.streak=-1
                else:
                    team2.streak+=(-1)
                messages.success(request,'Match has been forfeited by Team 2!')
            elif request.POST['purpose']=="bothff":
                matchtoupdate.replay='Forfeit'
                team1.losses+=1; team2.losses+=1
                team1.differential+=(-6); team2.differential+=(-6)
                team1.forfeit+=1; team2.forfeit+=1
                if team1.streak>-1:
                    team1.streak=-1
                else:
                    team1.streak+=(-1)
                if team2.streak>-1:
                    team2.streak=-1
                else:
                    team2.streak+=(-1)
                messages.success(request,'Match has been forfeited by both teams!')
            team1.save()
            team2.save()
            matchtoupdate.save()
            return redirect('league_playoffs',league_name=league_name)
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'leagueschedule': leagueschedule,
        'ishost': ishost,
        'playoffs': True,
        'playoffweeks':playoffweeks,
    }
    return render(request, 'schedule.html',context)

@check_if_subleague
@check_if_season
@login_required
def change_match_attribution(request,league_name,subleague_name,matchid):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    try:
        match=schedule.objects.get(pk=matchid)
        if match.replay == "Link":
            messages.error(request,f'A replay for that match does not exist!',extra_tags="danger")
            return redirect('league_schedule',league_name=league_name)
    except:
        return redirect('league_schedule',league_name=league_name)
    if request.user.is_staff==False:
        messages.error(request,f'Only staff may use this function',extra_tags="danger")
        return redirect('league_schedule',league_name=league_name)
    if request.method=="POST":
        form=ChangeMatchAttributionForm(request.POST,instance=match)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request,f'Match was updated!')
        return redirect('league_schedule',league_name=league_name)
    form=ChangeMatchAttributionForm(instance=match)
    context={
        'form':form,
        'league_name':league_name,
        'matchid':matchid,
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        }
    return render(request,"matchattribution.html",context)

class PokemonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = all_pokemon.objects.all().order_by('pokemon')

        if self.q:
            qs = qs.filter(pokemon__istartswith=self.q)

        return qs

@login_required
@check_if_subleague
@check_if_season
@check_if_host
def createroundrobinschedule(request,league_name,subleague_name):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    leaguesettings=league_settings.objects.get(league_name=subleague.league)
    needednumberofcoaches=leaguesettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=subleague.league)
    currentcoachescount=len(currentcoaches)
    if needednumberofcoaches != currentcoachescount: 
        messages.error(request,'You can only utilize season settings if you have designated the same number of coaches as available spots',extra_tags='danger')
        return redirect('individual_league_settings',league_name=league_name)
    existingmatches=schedule.objects.all().filter(season=seasonsettings).exclude(replay='Link')
    if existingmatches.count()>0:
        messages.error(request,'Matches already exist!',extra_tags='danger')
        return redirect('manage_seasons',league_name=league_name)
    schedule.objects.all().filter(season=seasonsettings).delete()
    #get conferences
    conferences=conference_name.objects.all().filter(league=subleague.league)
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
                    schedule.objects.create(season=seasonsettings,week=str(week+1),team1=conference[i],team2=conference[count-i-1])
                elif conference[i]==None:
                    interconf.append(conference[count-i-1])
                elif conference[count-i-1]==None:
                    interconf.append(conference[i])
            conference.insert(1, conference.pop())
        interconfteams.append(interconf)
    for i in range(len(interconfteams[0])):
        schedule.objects.create(season=seasonsettings,week=str(i+1),team1=interconfteams[0][i],team2=interconfteams[1][i])
    return redirect('manage_seasons',league_name=league_name)