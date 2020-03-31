from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

import math
import json
from datetime import datetime, timezone, timedelta
import pytz
from dal import autocomplete
from itertools import chain

from .models import *
from leagues.models import *
from pokemondatabase.models import *
from accounts.models import *
from .forms import *
from pokemondraftleague.customdecorators import check_if_subleague, check_if_league, check_if_season, check_if_team, check_if_host

@check_if_league
def league_detail(request,league_name):
    league_name=league_name.replace("_"," ")
    league_=league.objects.get(name=league_name)
    subleagues=league_.subleague.all().order_by('subleague')
    if subleagues.count()==1:
        loi=subleagues.first()
        return redirect('subleague_detail',league_name=league_name,subleague_name=loi.subleague)
    else:
        if league_.configuration.teambased:
            try:
                standings=[]
                league_teams=league_.leagueteam.all().order_by('-points','-differential')
                for item in league_teams:
                    item.wins=0; item.losses=0; item.ties=0; item.points=0; item.differential=0
                    teamschedule=[]
                    teamschedule_=schedule.objects.all().filter(Q(team1=item.child_teams.first())|Q(team2=item.child_teams.first())).order_by('duedate','week')
                    for match in teamschedule_:
                        #find opponent
                        opponent=None
                        if item==match.team1.parent_team:
                            opponent=match.team2.parent_team
                        elif item==match.team2.parent_team:
                            opponent=match.team1.parent_team
                        #weekly record
                        wins=0
                        losses=0
                        weeksmatches=schedule.objects.all().filter(Q(team1__parent_team=item)|Q(team2__parent_team=item)).filter(week=match.week).exclude(replay="Link").exclude(winner__isnull=True)
                        for m in weeksmatches:
                            if m.winner and m.winner.parent_team==item:
                                wins+=1 
                                item.differential+=1
                            else: 
                                losses+=1
                                item.differential+=-1
                        teamschedule.append([opponent,wins,losses,match.week])
                        #update records
                        unplayedgames=schedule.objects.all().filter(Q(team1__parent_team=item)|Q(team2__parent_team=item)).filter(week=match.week).filter(replay="Link")
                        if unplayedgames.count()==0:
                            if wins>losses:
                                item.wins+=1
                                item.points+=3
                            elif wins<losses:
                                item.losses+=1
                            else:
                                item.ties+=1
                                item.points+=1
                            item.save()
                    standings.append([item,teamschedule])
                numberofweeks=range(teamschedule_.count())
                context = {
                    'league': league_,
                    'league_name': league_name,
                    'subleagues':subleagues,
                    'leaguecomposite':True,
                    'apply':True,
                    'league_teams':league_teams,
                    'standings':standings,
                    'numberofweeks':numberofweeks,
                }
            except:
                context = {
                'league': league_,
                'league_name': league_name,
                'subleagues':subleagues,
                'leaguecomposite':True,
                'apply':True,
                'league_teams':league_teams,
                'standings':None,
                'numberofweeks':None,
                }
            return render(request, 'subleague_composite_detail.html',context)
        else:
            context = {
                'league': league_,
                'league_name': league_name,
                'leaguecomposite':True,
                'subleagues':subleagues,
            }
            return render(request, 'subleague_composite_no_teams.html',context)

@check_if_league
def teampage_detail(request,league_name,team_name):
    league_name=league_name.replace("_"," ")
    team_name=team_name.replace("_"," ")
    league_=league.objects.get(name=league_name)
    subleagues=league_.subleague.all().order_by('subleague')
    league_teams=league_.leagueteam.all().order_by('-points','-differential')
    team_of_interest=league_teams.get(name=team_name)
    leagueteam_teams_=team_of_interest.child_teams.all().order_by('-wins','losses','-differential','teamname')
    leagueteam_teams=[]
    for item in leagueteam_teams_:
        teamschedule=schedule.objects.filter(Q(team1=item)|Q(team2=item)).order_by('duedate','week')
        leagueteam_teams.append([item,teamschedule])
    standings=1
    for item in league_teams:
        if item == team_of_interest:
            break
        else:
            standings+=1
    teamschedule=[]
    teamschedule_=schedule.objects.all().filter(Q(team1=leagueteam_teams_.first())|Q(team2=leagueteam_teams_.first())).order_by('duedate','week')
    for match in teamschedule_:
        #find opponent
        opponent=None
        if team_of_interest==match.team1.parent_team:
            opponent=match.team2.parent_team
        elif team_of_interest==match.team2.parent_team:
            opponent=match.team1.parent_team
        #weekly record
        wins=0
        losses=0
        weeksmatches=schedule.objects.all().filter(Q(team1__parent_team=team_of_interest)|Q(team2__parent_team=team_of_interest)).filter(week=match.week).exclude(replay="Link").exclude(winner__isnull=True)
        for m in weeksmatches:
            if m.winner and m.winner.parent_team==team_of_interest:
                wins+=1 
            else: 
                losses+=1
        teamschedule.append([opponent,wins,losses,match.week])
    context = {
        'league': league_,
        'league_name': league_name,
        'subleagues':subleagues,
        'leaguecomposite':True,
        'apply':True,
        'league_teams':league_teams,
        'team_of_interest':team_of_interest,
        'leagueteam_teams':leagueteam_teams,
        'standings':standings,
        'teamschedule':teamschedule,
    }
    return render(request, 'leagueteam_detail.html',context)

@check_if_subleague
def subleague_detail(request,league_name,subleague_name):
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    settings=league_settings.objects.get(league_name=subleague.league)
    conferencelist=conference_name.objects.all().filter(subleague=subleague).order_by('id')
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
        season=seasonsetting.objects.get(subleague=subleague)
        timezone = pytz.timezone('UTC')
        elapsed=timezone.localize(datetime.now())-season.seasonstart
        timercurrentweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
        seasonstart=str(season.seasonstart)
    except:
        season=None
        timercurrentweek=None
        seasonstart=None
    try:
        sch=schedule.objects.all().filter(season__subleague=subleague).filter(duedate__gte=datetime.now()).order_by('duedate')
        currentweek=sch.filter(week=sch.first().week)
    except:
        currentweek=None
    context = {
        'subleague': subleague,
        'apply': apply,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'conferences': conferences,
        'season':season,
        'timercurrentweek': timercurrentweek,
        'seasonstart':seasonstart,
        'currentweek': currentweek,
        }
    return render(request, 'league_detail.html',context)

@check_if_league
@login_required
def league_apply(request,league_name):
    league_name=league_name.replace('_',' ')
    league_=league.objects.get(name=league_name)
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
                    return redirect('league_list')
                if request.method == 'POST':
                    form = LeagueApplicationForm(league_,request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request,'You have successfully applied to '+league_name+"!")
                        return redirect('league_detail',league_name=league_name)
                else:
                    form=None
                    form = LeagueApplicationForm(league_,initial={
                        'applicant': request.user,
                        'league_name': league_
                        })
                    
                context = {
                    'league': league_,
                    'form': form,
                }
                return render(request, 'leagueapplication.html',context)

@check_if_subleague
@check_if_season
@check_if_team
def team_page(request,league_name,subleague_name,team_abbreviation):
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    team=league_teams.get(teamabbreviation=team_abbreviation)
    teamroster=team.teamroster.all().order_by('id')
    matchs=schedule.objects.all().filter(season=season).filter(Q(team1=team)|Q(team2=team))
    results=matchs.exclude(replay="Link").order_by('-timestamp')
    upcoming=matchs.filter(replay="Link").order_by('duedate','week')[0:4]
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
    league_name=league_name.replace('_',' ')
    ##basic config
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    coachcount=league_teams.count()
    season=subleague.seasonsetting
    try:  
        site_settings = request.user.sitesettings
    except:
        user=User.objects.get(username="defaultuser")
        site_settings = user.sitesettings
    takenpokemon=roster.objects.all().filter(season=season).exclude(pokemon__isnull=True).values_list('pokemon',flat=True)
    availablepokemon=pokemon_tier.objects.all().exclude(tier__tiername="Banned").exclude(pokemon__id__in=takenpokemon).filter(subleague=subleague).order_by("-tier__tierpoints",'pokemon__pokemon')
    availablepokemonjson=[]
    for item in availablepokemon:
        availablepokemonjson.append([item.pokemon.pokemon,item.tier.tiername,item.tier.tierpoints,get_sprite_url(item.pokemon,site_settings.sprite),list(item.pokemon.types.all().values('typing'))])
    json.dumps(availablepokemonjson)
    tierchoices=leaguetiers.objects.all().filter(subleague=subleague).exclude(tiername="Banned").order_by('tiername')
    types=pokemon_type.objects.all().distinct('typing').values_list('typing',flat=True)
    draftlist=draft.objects.all().filter(season=season)
    currentpick=draftlist.filter(pokemon__isnull=True,skipped=False).order_by('picknumber').first()
    subleaguetiers=pokemon_tier.objects.filter(subleague=subleague)
    ##existing draftdata
    draftbyteam=[]
    iscoach=False
    for item in league_teams:
        pointsused=0
        pointsremaining=season.draftbudget
        teamdraft_=item.draftpicks.all()
        teamdraft=[]
        for item_ in teamdraft_:
            try:
                pkmn=item_.pokemon.pokemon
                points=subleaguetiers.get(pokemon=item_.pokemon).tier.tierpoints
                pointsremaining+=-points
                pointsused+=points
            except:
                pkmn="-"
                points="-"
            teamdraft.append([item_.picknumber,pkmn,points])
        draftbyteam.append([item,teamdraft,pointsused,pointsremaining])
        try:
            if item==currentpick.team: currentpoints=pointsremaining
        except:
            currentpoints=None
        if request.user==item.coach: 
            iscoach=True
            usercoach=item
    try:
        draftbyteam=sorted(draftbyteam, key=lambda x: x[1][0][0])
    except:
        pass
    #check for current leftpicks
    try:
        currentleftpicks=left_pick.objects.all().filter(season=season,coach=currentpick.team).order_by('id')
    except:
        currentleftpicks=left_pick.objects.none()
    if currentleftpicks.count()>0:
        for item in currentleftpicks:
            if item.pick.id not in takenpokemon:
                currentpick.pokemon=item.pick
                rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
                rosterspot.pokemon=item.pick
                senddraftpicktobot(currentpick,item.pick,subleague,draftlist)
                rosterspot.save()
                currentpick.save()
                item.delete()
                return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)  
            elif item.backup.id not in takenpokemon:
                currentpick.pokemon=item.backup
                rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
                rosterspot.pokemon=item.backup
                senddraftpicktobot(currentpick,item.backup,subleague,draftlist)
                rosterspot.save()
                currentpick.save()
                item.delete()
                return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)  
            else:
                item.delete()
        return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)    
    ##form handling
    if request.method=="POST":
        formpurpose=request.POST['formpurpose']
        if formpurpose=="Submit":
            draftpick=request.POST['draftpick']
            try:
                draftpick=all_pokemon.objects.get(pokemon=draftpick)
            except:
                messages.error(request,f'{draftpick} is not a pokemon!',extra_tags='danger')
                return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
            if draftpick.id in takenpokemon:
                messages.error(request,f'{draftpick.pokemon} has already been drafted!',extra_tags='danger')
                return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
            currentpick.pokemon=draftpick
            rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
            rosterspot.pokemon=draftpick
            rosterspot.save()
            currentpick.save()
            senddraftpicktobot(currentpick,draftpick,subleague,draftlist)
            messages.success(request,'Your draft pick has been saved!')
        elif formpurpose=="Skip":
            currentpick.skipped=True
            currentpick.save()
        elif formpurpose=="Skip Remaining Picks":
            currentpick.coach.draftpicks.all().filter(skipped=False,pokemon__isnull=True).update(skipped=True)
        #adding leftpick
        elif formpurpose=="Add":
            pick=request.POST['pick']
            backup=request.POST['backup']
            try: 
                pick=all_pokemon.objects.get(pokemon=pick)
            except:
                messages.error(request,f'{pick} is not a pokemon!',extra_tags='danger')
                return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
            if backup=="":
                backup=pick
            else:
                try: 
                    backup=all_pokemon.objects.get(pokemon=backup)
                except:
                    messages.error(request,f'{backup} is not a pokemon!',extra_tags='danger')
                    return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
            left_pick.objects.create(coach=usercoach,season=season,pick=pick,backup=backup)
        elif formpurpose=="Delete":
            leftpickid=request.POST['leftpickid']
            left_pick.objects.get(id=leftpickid).delete()
        return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
    try:
        draftprogress=round(draftlist.exclude(pokemon__isnull=True).count()/draftlist.count()*100,1)
    except:
        draftprogress="N/A"
    leftpicks=left_pick.objects.all().filter(season=season,coach__coach=request.user)
    context={
        'subleague':subleague,
        'league_name':league_name,
        'league_teams':league_teams,
        'draftlist': draftlist,
        'draftbyteam':draftbyteam,
        'draftprogress':draftprogress,
        'currentpick':currentpick,
        'currentpoints':currentpoints,
        'leftpicks':leftpicks,
        'iscoach':iscoach,
        'availablepokemon':availablepokemon,
        'availablepokemonjson':availablepokemonjson,
        'tierchoices':tierchoices,
        'types':types,
        'leaguepage': True,
    }
    return render(request, 'draft.html',context)

def senddraftpicktobot(currentpick,pokemon,subleague,draftlist):
    #send to bot
    text=f'The {currentpick.team.teamname} have drafted {pokemon.pokemon}'
    draftchannel=subleague.discord_settings.draftchannel
    try:
        upnext=draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.username
        upnextid=str(draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.profile.discordid)
    except:
        upnext="The draft has concluded"
        upnextid=""
    draft_announcements.objects.create(league=subleague.discord_settings.discordserver,league_name=subleague.league.name.replace(' ','%20'),text=text,upnext=upnext,draftchannel=draftchannel,upnextid=upnextid)
    return

@check_if_subleague
@check_if_season
def league_schedule(request,league_name,subleague_name):
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    season=subleague.seasonsetting
    seasonschedule=schedule.objects.all().filter(season=season).exclude(week__contains="Playoff").order_by('duedate','week')
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'seasonschedule':seasonschedule,
    }
    if request.method=="POST":
        if request.POST['purpose']=="t1pickem":
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
            return redirect('league_schedule',league_name=league_name,subleague_name=subleague_name)
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
            return redirect('league_schedule',league_name=league_name,subleague_name=subleague_name)
        else:
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            team1=matchtoupdate.team1
            team2=matchtoupdate.team2
            if request.POST['purpose']=="t1ff":
                matchtoupdate.replay=f'Team 1 Forfeits'
                matchtoupdate.winner=team2
                matchtoupdate.team2score=3
                team1.losses+=1; team2.wins+=1
                team1.differential+=(-3); team2.differential+=3
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
                matchtoupdate.replay=f'Team 2 Forfeits'
                matchtoupdate.winner=team1
                matchtoupdate.team1score=3
                team1.wins+=1; team2.losses+=1
                team1.differential+=3; team2.differential+=(-3)
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
                team1.differential+=(-3); team2.differential+=(-3)
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
            discordserver=subleague.discord_settings.discordserver
            discordchannel=subleague.discord_settings.replaychannel
            title=f"Week: {matchtoupdate.week}. {matchtoupdate.team1.teamname} vs {matchtoupdate.team2.teamname}: {matchtoupdate.replay}."
            replay_announcements.objects.create(
                league = discordserver,
                league_name = league_.name,
                text = title,
                replaychannel = discordchannel
            )
            return redirect('league_schedule',league_name=league_name,subleague_name=subleague_name)
    return render(request, 'schedule.html',context)

@check_if_league
def total_league_schedule(request,league_name):
    league_name=league_name.replace("_"," ")
    league_=league.objects.get(name=league_name)
    seasonschedule=schedule.objects.all().filter(season__league__name=league_name).exclude(week__contains="Playoff").order_by('duedate','week')
    subleagues=league_.subleague.all().order_by('subleague')
    league_teams=league_.leagueteam.all().order_by('-points','-differential')
    context = {
        'league_name': league_name,
        'seasonschedule':seasonschedule,
        'includesubleague':True,
        'leaguecomposite':True,
        'subleagues':subleagues,
        'league_teams':league_teams,
    }
    if request.method=="POST":
        if request.POST['purpose']=="t1pickem":
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
            return redirect('total_league_schedule',league_name=league_name)
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
            return redirect('total_league_schedule',league_name=league_name)
        else:
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            team1=matchtoupdate.team1
            team2=matchtoupdate.team2
            if request.POST['purpose']=="t1ff":
                matchtoupdate.replay=f'Team 1 Forfeits'
                matchtoupdate.winner=team2
                matchtoupdate.team2score=3
                team1.losses+=1; team2.wins+=1
                team1.differential+=(-3); team2.differential+=3
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
                matchtoupdate.replay=f'Team 2 Forfeits'
                matchtoupdate.winner=team1
                matchtoupdate.team1score=3
                team1.wins+=1; team2.losses+=1
                team1.differential+=3; team2.differential+=(-3)
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
                team1.differential+=(-3); team2.differential+=(-3)
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
            discordserver=matchtoupdate.season.subleague.discord_settings.discordserver
            discordchannel=matchtoupdate.season.subleague.discord_settings.replaychannel
            title=f"Week: {matchtoupdate.week}. {matchtoupdate.team1.teamname} vs {matchtoupdate.team2.teamname}: {matchtoupdate.replay}."
            replay_announcements.objects.create(
                league = discordserver,
                league_name = league_.name,
                text = title,
                replaychannel = discordchannel
            )
            return redirect('total_league_schedule',league_name=league_name)
    return render(request, 'schedule.html',context)

@check_if_league
def total_league_playoffs(request,league_name):
    league_name=league_name.replace("_"," ")
    league_=league.objects.get(name=league_name)
    seasonschedule=schedule.objects.all().filter(season__league__name=league_name).filter(week__contains="Playoff").order_by('duedate','week')
    subleagues=league_.subleague.all().order_by('subleague')
    league_teams=league_.leagueteam.all().order_by('-points','-differential')
    context = {
        'league_name': league_name,
        'seasonschedule':seasonschedule,
        'includesubleague':True,
        'leaguecomposite':True,
        'subleagues':subleagues,
        'league_teams':league_teams,
    }
    if request.method=="POST":
        if request.POST['purpose']=="t1pickem":
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
            return redirect('total_league_schedule',league_name=league_name)
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
            return redirect('total_league_schedule',league_name=league_name)
        else:
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            team1=matchtoupdate.team1
            team2=matchtoupdate.team2
            if request.POST['purpose']=="t1ff":
                matchtoupdate.replay=f'Team 1 Forfeits'
                matchtoupdate.winner=team2
                matchtoupdate.team2score=3
                team1.losses+=1; team2.wins+=1
                team1.differential+=(-3); team2.differential+=3
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
                matchtoupdate.replay=f'Team 2 Forfeits'
                matchtoupdate.winner=team1
                matchtoupdate.team1score=3
                team1.wins+=1; team2.losses+=1
                team1.differential+=3; team2.differential+=(-3)
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
                team1.differential+=(-3); team2.differential+=(-3)
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
            discordserver=matchtoupdate.season.subleague.discord_settings.discordserver
            discordchannel=matchtoupdate.season.subleague.discord_settings.replaychannel
            title=f"Week: {matchtoupdate.week}. {matchtoupdate.team1.teamname} vs {matchtoupdate.team2.teamname}: {matchtoupdate.replay}."
            replay_announcements.objects.create(
                league = discordserver,
                league_name = league_.name,
                text = title,
                replaychannel = discordchannel
            )
            return redirect('total_league_schedule',league_name=league_name)
    return render(request, 'schedule.html',context)

@check_if_league
def composite_weekly_matchup(request,league_name,week,teamname):
    league_name=league_name.replace("_"," ")
    teamname=teamname.replace("_"," ")
    league_=league.objects.get(name=league_name)
    seasonschedule=schedule.objects.all().filter(season__league__name=league_name,week=week).filter(Q(team1__parent_team__name=teamname)|Q(team2__parent_team__name=teamname)).order_by('duedate','week')
    subleagues=league_.subleague.all().order_by('subleague')
    league_teams=league_.leagueteam.all().order_by('-points','-differential')
    context = {
        'league_name': league_name,
        'seasonschedule':seasonschedule,
        'includesubleague':True,
        'leaguecomposite':True,
        'subleagues':subleagues,
        'league_teams':league_teams,
    }
    if request.method=="POST":
        if request.POST['purpose']=="t1pickem":
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
            return redirect('total_league_schedule',league_name=league_name)
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
            return redirect('total_league_schedule',league_name=league_name)
        else:
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            team1=matchtoupdate.team1
            team2=matchtoupdate.team2
            if request.POST['purpose']=="t1ff":
                matchtoupdate.replay=f'Team 1 Forfeits'
                matchtoupdate.winner=team2
                matchtoupdate.team2score=3
                team1.losses+=1; team2.wins+=1
                team1.differential+=(-3); team2.differential+=3
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
                matchtoupdate.replay=f'Team 2 Forfeits'
                matchtoupdate.winner=team1
                matchtoupdate.team1score=3
                team1.wins+=1; team2.losses+=1
                team1.differential+=3; team2.differential+=(-3)
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
                team1.differential+=(-3); team2.differential+=(-6)
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
            discordserver=matchtoupdate.season.subleague.discord_settings.discordserver
            discordchannel=matchtoupdate.season.subleague.discord_settings.replaychannel
            title=f"Week: {matchtoupdate.week}. {matchtoupdate.team1.teamname} vs {matchtoupdate.team2.teamname}: {matchtoupdate.replay}."
            replay_announcements.objects.create(
                league = discordserver,
                league_name = league_.name,
                text = title,
                replaychannel = discordchannel
            )
            return redirect('total_league_schedule',league_name=league_name)
    return render(request, 'schedule.html',context)

@check_if_subleague
@check_if_season
def league_matchup(request,league_name,subleague_name,matchid):
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    try:
        match=schedule.objects.get(id=matchid)
    except:
        messages.error(request,'Match does not exist!',extra_tags='danger')
        return redirect('league_schedule',league_name=league_name,subleague_name=subleague_name)
    team1roster=roster.objects.filter(season=season,team=match.team1,pokemon__isnull=False).order_by('pokemon__pokemon')
    team2roster=roster.objects.filter(season=season,team=match.team2,pokemon__isnull=False).order_by('pokemon__pokemon')
    moves=['Stealth Rock','Spikes','Toxic Spikes','Sticky Web','Defog','Rapid Spin','Heal Bell','Aromatherapy','Wish']
    context = {
        'subleague':subleague,
        'match':match,
        'team1roster':team1roster,
        'team2roster':team2roster,
        'moves':moves,
    }
    return render(request, 'matchup.html',context)

@check_if_subleague
@check_if_season
def league_rules(request,league_name,subleague_name):
    league_name=league_name.replace('_',' ')
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
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    season=subleague.seasonsetting
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    ruleset=rule.objects.get(season=season)
    if request.method=="POST":
        form=RuleChangeForm(request.POST,instance=ruleset)
        if form.is_valid():
            form.save()
            messages.success(request,'Rules have been updated!')
        return redirect('league_rules',league_name=league_name,subleague_name=subleague_name)
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
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    tierlist_=pokemon_tier.objects.all().filter(subleague=subleague).exclude(tier__tiername="Banned").order_by('-tier__tierpoints','pokemon__pokemon')
    tierchoices=leaguetiers.objects.all().filter(subleague=subleague).exclude(tiername="Banned").order_by('tiername')
    rosterlist=roster.objects.all().filter(season__subleague=subleague)
    rosterlist_=list(rosterlist.values_list('pokemon',flat=True))
    try:  
        site_settings = request.user.sitesettings
    except:
        user=User.objects.get(username="defaultuser")
        site_settings = user.sitesettings
    tiersjson=[]
    tierdictjson={}
    for item in tierchoices:
        tierdictjson[f'{item.tiername} ({item.tierpoints} pts)']=[]
    for item in tierlist_:
        poi=item.pokemon
        types=[]
        for item2 in poi.types.all():
            types.append(item2.typing)
        if item.pokemon.id in rosterlist_:
            owner=rosterlist.get(pokemon__id=item.pokemon.id)
            tiersjson.append([poi.pokemon,f"Signed by {owner.team.teamabbreviation}",item.tier.tiername,item.tier.tierpoints,get_sprite_url(poi,site_settings.sprite),types,poi.hp,poi.attack,poi.defense,poi.s_attack,poi.s_defense,poi.speed,poi.bst])
            tierdictjson[f'{item.tier.tiername} ({item.tier.tierpoints} pts)'].append([poi.pokemon,get_sprite_url(poi,site_settings.sprite),owner.team.teamabbreviation])
        else:
            try:
                tiersjson.append([poi.pokemon,f"FREE",item.tier.tiername,item.tier.tierpoints,get_sprite_url(poi,site_settings.sprite),types,poi.hp,poi.attack,poi.defense,poi.s_attack,poi.s_defense,poi.speed,poi.bst])
                tierdictjson[f'{item.tier.tiername} ({item.tier.tierpoints} pts)'].append([poi.pokemon,get_sprite_url(poi,site_settings.sprite),'FREE'])
            except:
                banned=leaguetiers.objects.all().filter(subleague=subleague).get(tiername="Banned")
                item.tier=banned
                item.save()
    types=pokemon_type.objects.all().distinct('typing').values_list('typing',flat=True)
    json.dumps(tiersjson)
    json.dumps(tierdictjson)
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'types':types,
        'tierchoices':tierchoices,
        'tiersjson':tiersjson,
        'tierdictjson':tierdictjson,
    }
    return render(request, 'tiers.html',context)

def get_sprite_url(poi,arg):
    if arg=="swsh/ani/standard/PKMN.gif":
        string=poi.sprite.dexani.url
    elif arg=="swsh/ani/shiny/PKMN.gif":
        string=poi.sprite.dexanishiny.url
    elif arg=="swsh/png/standard/PKMN.png":
        string=poi.sprite.dex.url
    elif arg=="swsh/png/shiny/PKMN.png":
        string=poi.sprite.dexshiny.url
    elif arg=="bw/png/standard/PKMN.png":
        string=poi.sprite.bw.url
    elif arg=="bw/png/shiny/PKMN.png":
        string=poi.sprite.bwshiny.url
    elif arg=="afd/png/standard/PKMN.png":
        string=poi.sprite.afd.url
    elif arg=="afd/png/shiny/PKMN.png":
        string=poi.sprite.afdshiny.url
    return string

@login_required
@check_if_subleague
@check_if_season
def freeagency(request,league_name,subleague_name):
    ##basic config
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    season=subleague.seasonsetting
    try:  
        site_settings = request.user.sitesettings
    except:
        user=User.objects.get(username="defaultuser")
        site_settings = user.sitesettings
    takenpokemon=list(roster.objects.all().filter(season=season).exclude(pokemon__isnull=True).values_list('pokemon',flat=True))
    pendingfreeagency=free_agency.objects.all().filter(executed=False,season=season)
    pendingdrops=list(pendingfreeagency.values_list('droppedpokemon',flat=True))
    pendingadds=list(pendingfreeagency.values_list('addedpokemon',flat=True))
    takenpokemon=takenpokemon+pendingadds
    for item in pendingdrops:
        try:
            takenpokemon.remove(item)
        except:
            pass
    availablepokemon=pokemon_tier.objects.all().exclude(tier__tiername="Banned").exclude(pokemon__id__in=takenpokemon).filter(subleague=subleague).order_by("-tier__tierpoints",'pokemon__pokemon')
    availablepokemonjson=[]
    for item in availablepokemon:
        availablepokemonjson.append([item.pokemon.pokemon,item.tier.tiername,item.tier.tierpoints,get_sprite_url(item.pokemon,site_settings.sprite),list(item.pokemon.types.all().values('typing'))])
    tierchoices=leaguetiers.objects.all().filter(subleague=subleague).exclude(tiername="Banned").order_by('tiername')
    types=pokemon_type.objects.all().distinct('typing').values_list('typing',flat=True)
    userroster=roster.objects.all().filter(season=season,team__coach=request.user)
    pointsremaining=season.draftbudget
    for item in userroster:
        pointsremaining+=-pokemon_tier.objects.filter(subleague=subleague).get(pokemon=item.pokemon).tier.tierpoints
    try:
        coi=subleague.subleague_coachs.all().filter(Q(coach=request.user)|Q(teammate=request.user)).first()
        droppedpokemon=coi.teamroster.all()
        form=FreeAgencyForm(droppedpokemon,availablepokemon,initial={
            'coach':coi,
            'season':season,
        })
    except Exception as e:
        print(e)
        form=None
    if request.method=="POST":
        formpurpose=request.POST['formpurpose']
        if formpurpose=="Submit":
            form=FreeAgencyForm(droppedpokemon,availablepokemon,request.POST)
            if form.is_valid():
                faoi=form.save()
                timeadded=faoi.timeadded
                seasonstart=season.seasonstart
                if timeadded>=seasonstart:
                    try:
                        associatedschedule=season.schedule.all().filter(duedate__isnull=False)
                        weekeffective=associatedschedule.filter(duedate__gt=timeadded).first()
                        weekeffective=associatedschedule.filter(duedate__gt=weekeffective.duedate).first().week
                    except:
                        elapsed=timeadded-seasonstart
                        weekeffective=math.ceil(elapsed.days/7)
                faoi.weekeffective=weekeffective
                faoi.save()
                discordserver=subleague.discord_settings.discordserver
                discordchannel=subleague.discord_settings.freeagencychannel
                title=f"The {coi.teamname} have used a free agency to drop {faoi.droppedpokemon.pokemon} for {faoi.addedpokemon.pokemon}. Effective Week {weekeffective}."
                messages.success(request,f'You free agency request has been added to the queue and will be implemented following completion of this week\'s match!')
                freeagency_announcements.objects.create(league = discordserver,league_name = subleague.league.name,text = title,freeagencychannel = discordchannel)
            else:
                print(form.errors)
            return redirect('free_agency',league_name=league_name,subleague_name=subleague_name)
        elif formpurpose=="Undo":
            ooi=free_agency.objects.get(id=request.POST['freeagencyid'])
            free_agency.objects.filter(season=season,addedpokemon=ooi.droppedpokemon,executed=False).delete()
            ooi.delete()
            return redirect('free_agency',league_name=league_name,subleague_name=subleague_name)
    fa_remaining=season.freeagenciesallowed-free_agency.objects.all().filter(season=season,coach__coach=request.user).count()
    completedfreeagency=free_agency.objects.all().filter(executed=True,season=season)
    personalfreeagency=free_agency.objects.all().filter(season=season,coach__coach=request.user)
    context = {
        'availablepokemon':availablepokemon,
        'availablepokemonjson':availablepokemonjson,
        'tierchoices':tierchoices,
        'types':types,
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'fa_remaining':fa_remaining,
        'pendingfreeagency':pendingfreeagency,
        'completedfreeagency':completedfreeagency,
        'personalfreeagency':personalfreeagency,
        'userroster':userroster,
        'pointsremaining':pointsremaining,
        'form':form,
    }
    return render(request, 'freeagency.html',context)

@check_if_subleague
@check_if_season
def league_leaders(request,league_name,subleague_name):
    league_name=league_name.replace('_',' ')
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

@check_if_league
def composite_league_leaders(request,league_name):
    league_name=league_name.replace('_',' ')
    league_=league.objects.get(name=league_name)
    leagueleaders=roster.objects.all().filter(season__league=league_,gp__gt=0).order_by('-kills','-differential')
    subleagues=league_.subleague.all().order_by('subleague')
    league_teams=league_.leagueteam.all().order_by('-points','-differential')
    context = {
        'league_teams': league_teams,
        'league_name': league_name,
        'leagueleaders': leagueleaders,
        'includesubleague':True,
        'leaguecomposite':True,
        'subleagues':subleagues,
        'league_teams':league_teams,
    }
    return render(request, 'leagueleaders.html',context)

@login_required
@check_if_subleague
@check_if_season
def trading_view(request,league_name,subleague_name):
    ##basic config
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    try:
        league_teams.get(coach=request.user)
        iscoach=True
    except:
        iscoach=False
    season=subleague.seasonsetting
    takenpokemon_=roster.objects.all().filter(season=season).exclude(pokemon__isnull=True).exclude(team__coach=request.user)
    takenpokemon=takenpokemon_.values_list('pokemon',flat=True)
    availablepokemon_=pokemon_tier.objects.all().exclude(tier__tiername="Banned").filter(pokemon__id__in=takenpokemon).filter(subleague=subleague).order_by("-tier__tierpoints",'pokemon__pokemon')
    availablepokemon=[]
    for item in availablepokemon_:
        rosterspot=takenpokemon_.get(pokemon=item.pokemon)
        availablepokemon.append([item,rosterspot])
    tierchoices=leaguetiers.objects.all().filter(subleague=subleague).exclude(tiername="Banned").order_by('tiername')
    types=pokemon_type.objects.all().distinct('typing').values_list('typing',flat=True)
    userroster=roster.objects.all().filter(season=season,team__coach=request.user)
    pointsremaining=season.draftbudget
    for item in userroster:
        pointsremaining+=-pokemon_tier.objects.filter(subleague=subleague).get(pokemon=item.pokemon).tier.tierpoints
    if request.method=="POST":
        formpurpose=request.POST['formpurpose']
        if formpurpose=="Submit":
            addedpokemon=request.POST['addedpokemon']
            droppedpokemon=roster.objects.get(id=request.POST['droppedpokemon'])
            try:
                addedpokemon=takenpokemon_.get(pokemon__pokemon=addedpokemon)
            except:
                messages.error(request,f'{addedpokemon} is not a pokemon on another roster!',extra_tags='danger')
                return redirect('trading',league_name=league_name,subleague_name=subleague_name)
            traderequest=trade_request.objects.create(offeredpokemon=droppedpokemon,requestedpokemon=addedpokemon)
            #send message
            sender=traderequest.offeredpokemon.team.coach
            recipient=traderequest.requestedpokemon.team.coach
            messagebody=f"Hello, I just sent you a new trade request in the {subleague.subleague} subleague of {subleague.league.name}. Check it out at: http://pokemondraftleague.online/leagues/{subleague.league.name}/{subleague.subleague}/trading/"
            inbox.objects.create(sender=sender,recipient=recipient,messagesubject="New Trade Proposal",messagebody=messagebody)
            return redirect('trading',league_name=league_name,subleague_name=subleague_name)
        elif formpurpose=="Accept":
            try:
                traderequest=trade_request.objects.get(id=request.POST['tradeid'])
            except:
                messages.error(request,f'Trade request does not exist!',extra_tags='danger')
                return redirect('trading',league_name=league_name,subleague_name=subleague_name)
            offered=traderequest.offeredpokemon
            requested=traderequest.requestedpokemon
            offered.zuser="N"
            requested.zuser="N"
            offered.save()
            requested.save()
            offeredteam=offered.team
            requestedteam=requested.team
            toi=trading.objects.create(coach=offeredteam,season=offered.season,droppedpokemon=offered.pokemon,addedpokemon=requested.pokemon)
            trading.objects.create(coach=requestedteam,season=requested.season,droppedpokemon=requested.pokemon,addedpokemon=offered.pokemon)
            recipient=traderequest.offeredpokemon.team.coach
            sender=traderequest.requestedpokemon.team.coach
            messagebody=f"Hello, I'm happy to accept your trade request in the {subleague.subleague} subleague of {subleague.league.name}. Thank you!"
            inbox.objects.create(sender=sender,recipient=recipient,messagesubject="Trade Request Accepted",messagebody=messagebody)
            discordserver=subleague.discord_settings.discordserver
            discordchannel=subleague.discord_settings.tradechannel
            timeadded=toi.timeadded
            seasonstart=season.seasonstart
            if timeadded<seasonstart:
                weekeffective=1
            else:
                try:
                    associatedschedule=season.schedule.all().filter(duedate__isnull=False)
                    weekeffective=associatedschedule.filter(duedate__gt=timeadded).first()
                    weekeffective=associatedschedule.filter(duedate__gt=weekeffective.duedate).first().week
                except:
                    elapsed=timeadded-seasonstart
                    weekeffective=math.ceil(elapsed.days/7)
            toi.weekeffective=weekeffective
            toi.save()
            title=f"The {offeredteam.teamname} have agreed to trade their {offered.pokemon.pokemon} to the {requestedteam.teamname} for their {requested.pokemon.pokemon}. Effective Week {weekeffective}."
            trading_announcements.objects.create(
                league = discordserver,
                league_name = subleague.league.name,
                text = title,
                tradingchannel = discordchannel
            )
            traderequest.delete()
            return redirect('trading',league_name=league_name,subleague_name=subleague_name)
        elif formpurpose=="Reject":
            try:
                traderequest=trade_request.objects.get(id=request.POST['tradeid'])
                recipient=traderequest.offeredpokemon.team.coach
                sender=traderequest.requestedpokemon.team.coach
                messagebody=f"Hello, I'm sorry but I'm not interested in your trade request in the {subleague.subleague} subleague of {subleague.league.name}. Sorry!"
                inbox.objects.create(sender=sender,recipient=recipient,messagesubject="Trade Request Rejected",messagebody=messagebody)
                traderequest.delete()
            except:
                messages.error(request,f'Trade request does not exist!',extra_tags='danger')
            return redirect('trading',league_name=league_name,subleague_name=subleague_name)
        elif formpurpose=="Rescind":
            try:
                traderequest=trade_request.objects.get(id=request.POST['tradeid'])
                sender=traderequest.offeredpokemon.team.coach
                recipient=traderequest.requestedpokemon.team.coach
                messagebody=f"Hello, I just rescinded my trade request in the {subleague.subleague} subleague of {subleague.league.name}. Sorry!"
                inbox.objects.create(sender=sender,recipient=recipient,messagesubject="Trade Request Rescinded",messagebody=messagebody)
                traderequest.delete()
            except:
                messages.error(request,f'Trade request does not exist!',extra_tags='danger')
            return redirect('trading',league_name=league_name,subleague_name=subleague_name)
        elif formpurpose=="Undo":
            try:
                trade=trading.objects.get(id=request.POST['tradeid'])
                if trade.id%2==0:
                    tradepartner=trading.objects.get(id=int(request.POST['tradeid'])+1)
                else:
                    tradepartner=trading.objects.get(id=int(request.POST['tradeid'])-1)
                recipient=tradepartner.coach.coach
                sender=trade.coach.coach
                messagebody=f"Hello, I'm sorry but I've decided to cancel our trade in the {subleague.subleague} subleague of {subleague.league.name}. Sorry!"
                inbox.objects.create(sender=sender,recipient=recipient,messagesubject="Trade Cancelled",messagebody=messagebody)
                trade.delete()
                tradepartner.delete()
            except Exception as e:
                raise(e)
                messages.error(request,f'Trade does not exist!',extra_tags='danger')
            return redirect('trading',league_name=league_name,subleague_name=subleague_name)
    trades_remaining=season.tradesallowed-trading.objects.all().filter(season=season,coach__coach=request.user).count()
    trading.objects.all().filter(id__gte=34,id__lte=37).delete()
    pendingtrades=trading.objects.all().filter(executed=False,season=season)
    completedtrades=trading.objects.all().filter(executed=True,season=season)
    personaltrades_=trading.objects.all().filter(season=season,coach__coach=request.user)
    personaltrades=[]
    for item in personaltrades_:
        if item.id%2==0:
            tradepartner=trading.objects.get(id=item.id+1)
        else:
            tradepartner=trading.objects.get(id=item.id-1)
        personaltrades.append([item,tradepartner])
    receivedtrades=trade_request.objects.filter(requestedpokemon__team__coach=request.user)
    proposedtrades=trade_request.objects.filter(offeredpokemon__team__coach=request.user)
    context = {
        'availablepokemon':availablepokemon,
        'tierchoices':tierchoices,
        'types':types,
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'trades_remaining':trades_remaining,
        'pendingtrades':pendingtrades,
        'completedtrades':completedtrades,
        'personaltrades':personaltrades,
        'userroster':userroster,
        'pointsremaining':pointsremaining,
        'receivedtrades':receivedtrades,
        'proposedtrades':proposedtrades,
        'iscoach':iscoach,
    }
    return render(request, 'trading.html',context)

@check_if_subleague
@check_if_season
def league_hall_of_fame(request,league_name,subleague_name):
    league_name=league_name.replace('_',' ')
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
    league_name=league_name.replace('_',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    season=subleague.seasonsetting
    seasonschedule=schedule.objects.all().filter(season=season).filter(week__contains="Playoff").order_by('duedate','week')
    context = {
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'league_name': league_name,
        'seasonschedule':seasonschedule,
    }
    if request.method=="POST":
        if request.POST['purpose']=="t1pickem":
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
            return redirect('league_schedule',league_name=league_name,subleague_name=subleague_name)
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
            return redirect('league_schedule',league_name=league_name,subleague_name=subleague_name)
        else:
            matchtoupdate=schedule.objects.get(id=request.POST['matchid'])
            team1=matchtoupdate.team1
            team2=matchtoupdate.team2
            if request.POST['purpose']=="t1ff":
                matchtoupdate.replay=f'Team 1 Forfeits'
                matchtoupdate.winner=team2
                team1.losses+=1; team2.wins+=1
                team1.differential+=(-3); team2.differential+=3
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
                matchtoupdate.replay=f'Team 2 Forfeits'
                matchtoupdate.winner=team1
                team1.wins+=1; team2.losses+=1
                team1.differential+=3; team2.differential+=(-3)
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
                team1.differential+=(-3); team2.differential+=(-3)
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
            discordserver=subleague.discord_settings.discordserver
            discordchannel=subleague.discord_settings.replaychannel
            title=f"Week: {matchtoupdate.week}. {matchtoupdate.team1.teamname} vs {matchtoupdate.team2.teamname}: {matchtoupdate.replay}."
            replay_announcements.objects.create(
                league = discordserver,
                league_name = league_.name,
                text = title,
                replaychannel = discordchannel
            )
            return redirect('league_schedule',league_name=league_name,subleague_name=subleague_name)
    return render(request, 'schedule.html',context)

@login_required
def change_match_attribution(request,matchid):
    try:
        match=schedule.objects.get(pk=matchid)
        if match.replay == "Link":
            messages.error(request,f'A replay for that match does not exist!',extra_tags="danger")
            return redirect('home')
    except:
        return redirect('home')
    if request.user.is_staff==False:
        messages.error(request,f'Only staff may use this function',extra_tags="danger")
        return redirect('home')
    if request.method=="POST":
        form=ChangeMatchAttributionForm(request.POST,instance=match)
        if form.is_valid():
            form.save()
            messages.success(request,f'Match was updated!')
        return redirect('home')
    form=ChangeMatchAttributionForm(instance=match)
    context={
        'form':form,
        'matchid':matchid,
        }
    return render(request,"matchattribution.html",context)

class PokemonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = all_pokemon.objects.all().order_by('pokemon')

        if self.q:
            qs = qs.filter(pokemon__istartswith=self.q)

        return qs