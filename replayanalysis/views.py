from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import json
from datetime import datetime
import time
from background_task import background

from .models import *
from .forms import *
from leagues.models import *
from pokemonadmin.models import *
from accounts.models import showdownalts, inbox
from .NewParser.parser import *
from .helperfunctions import *
from pokemondraftleague.customdecorators import check_if_subleague, check_if_league, check_if_season, check_if_team, check_if_host, check_if_match, check_if_clad

def replay_analysis(request):
    if request.method=="POST":
        form = MatchReplayForm(request.POST)
        if form.is_valid():
            clad=User.objects.get(username="claduva")
            url=form.cleaned_data['url']
            try:    
                results = newreplayparse(url)
                if len(results['errormessage'])!=0 and request.user!=clad:
                    inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url)
            except Exception as e:
                raise(e)
                if request.user != clad:
                    inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url)
                messages.error(request,f'There was an error processing your replay. claduva has been notified.',extra_tags="danger")
            context={
                'results': results,
            }
            return render(request,"replayanalysisresults.html",context)
    form=MatchReplayForm()
    context={
        'form': form,
        'submission': True,
    }
    return  render(request,"replayanalysisform.html",context)

@check_if_subleague
@check_if_season
@check_if_match
@login_required
def upload_league_replay(request,league_name,subleague_name,matchid):
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    match=schedule.objects.get(pk=matchid)
    if match.replay != "Link":
        messages.error(request,f'A replay for that match already exists!',extra_tags="danger")
        return redirect('league_schedule',league_name=league_name,subleague_name=subleague.subleague)
    if subleague.league.settings.platform in ['Showdown','Youtube Showdown']:
        if request.method=="POST":
            form = LeagueReplayForm(request.POST,instance=match)
            if form.is_valid():
                clad=User.objects.get(username="claduva")
                url=form.cleaned_data['replay']
                try:    
                    results = newreplayparse(url)
                except:
                    inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url)
                    messages.error(request,f'There was an error processing your replay. claduva has been notified.',extra_tags="danger")
                    return redirect('league_schedule',league_name=league_name,subleague_name=subleague.subleague)
                coach1=results['team1']['coach']
                coach2=results['team2']['coach']
                try:
                    coach1alt=showdownalts.objects.all().get(showdownalt=coach1)
                    coach1team=coachdata.objects.all().filter(league_name=subleague.league).get(Q(coach=coach1alt.user)|Q(teammate=coach1alt.user))
                except:
                    messages.error(request,f'A matching showdown alt for {coach1} was not found!',extra_tags='danger')
                    return redirect('league_schedule',league_name=league_name,subleague_name=subleague.subleague)
                try:
                    coach2alt=showdownalts.objects.all().get(showdownalt=coach2)
                    coach2team=coachdata.objects.all().filter(league_name=subleague.league).get(Q(coach=coach2alt.user)|Q(teammate=coach2alt.user))
                except:
                    messages.error(request,f'A matching showdown alt for {coach2} was not found!',extra_tags='danger')
                    return redirect('league_schedule',league_name=league_name,subleague_name=subleague.subleague)
                if len(results['errormessage'])==0:
                    save_league_replay(request,results,match,coach1team,coach2team,form,subleague)
                else:
                    inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url)
                    messages.error(request,f'There was an error processing your replay. claduva has been notified.',extra_tags="danger")
                    return redirect('league_schedule',league_name=league_name,subleague_name=subleague.subleague)
                context={
                    'results':results,
                    'team1name':coach1team,
                    'team2name':coach2team,
                    'league_name':league_name,
                    'subleague': subleague,
                    'leaguepage': True,
                    'league_teams': league_teams,
                }
                return render(request,"replayanalysisresults.html",context)
        form=LeagueReplayForm(instance=match,initial={"replay":""})
        manual=False
    else:
        if request.method=="POST":
            form = ManualLeagueReplayForm(match,request.POST)
            if form.is_valid():
                data=update_manual_match(match,form,request)
                context={
                    'manualreplay':data,
                    'league_name':league_name,
                    'subleague': subleague,
                    'leaguepage': True,
                    'league_teams': league_teams,
                }
                return render(request,"manualreplayresults.html",context)
        form=ManualLeagueReplayForm(match,initial={
        'match':match,
        't1pokemon1kills':0,'t1pokemon2kills':0,'t1pokemon3kills':0,'t1pokemon4kills':0,'t1pokemon5kills':0,'t1pokemon6kills':0,
        't2pokemon1kills':0,'t2pokemon2kills':0,'t2pokemon3kills':0,'t2pokemon4kills':0,'t2pokemon5kills':0,'t2pokemon6kills':0,
        't1pokemon1death':0,'t1pokemon2death':0,'t1pokemon3death':0,'t1pokemon4death':0,'t1pokemon5death':0,'t1pokemon6death':0,
        't2pokemon1death':0,'t2pokemon2death':0,'t2pokemon3death':0,'t2pokemon4death':0, 't2pokemon5death':0,'t2pokemon6death':0,
        })
        manual=True
    context={
        'form': form,
        'submission': True,
        'league_name':league_name,
        'matchid':matchid,
        'subleague': subleague,
        'leaguepage': True,
        'league_teams': league_teams,
        'manual':manual,
    }
    return  render(request,"replayanalysisform.html",context)

def save_league_replay(request,results,match,team1,team2,form,subleague):
    try: 
        match.match_replay
        messages.error(request,f'A replay for that match already exists!',extra_tags="danger")
        return
    except:
        pass
    #iterate through team 1
    team1roster=team1.teamroster.all()
    objectstosave=[form]
    erroritems=[]
    for mon in results['team1']['roster']:
        foundmon,erroritems=pokemonsearch(mon['pokemon'],team1roster,erroritems)
        if foundmon:
            #update stats
            foundmon.kills+=mon['kills']
            foundmon.deaths+=mon['deaths']
            foundmon.differential+=mon['kills']-mon['deaths']
            foundmon.gp+=1
            foundmon.gw+=results['team1']['wins']
            foundmon.support+=mon['support']
            foundmon.damagedone+=mon['damagedone']
            foundmon.hphealed+=mon['hphealed']
            foundmon.luck+=mon['luck']
            foundmon.remaininghealth+=mon['remaininghealth']
            #append to save
            objectstosave.append(foundmon)
            #iterate moves
            iterate_moves(mon['moves'],team1,foundmon,results['replay'])
    #iterate through team 2
    team2roster=team2.teamroster.all()
    for mon in results['team2']['roster']:
        foundmon,erroritems=pokemonsearch(mon['pokemon'],team2roster,erroritems)
        if foundmon:
            #update stats
            foundmon.kills+=mon['kills']
            foundmon.deaths+=mon['deaths']
            foundmon.differential+=mon['kills']-mon['deaths']
            foundmon.gp+=1
            foundmon.gw+=results['team2']['wins']
            foundmon.support+=mon['support']
            foundmon.damagedone+=mon['damagedone']
            foundmon.hphealed+=mon['hphealed']
            foundmon.luck+=mon['luck']
            foundmon.remaininghealth+=mon['remaininghealth']
            #append to save
            objectstosave.append(foundmon)
            #iterate moves
            iterate_moves(mon['moves'],team2,foundmon,results['replay'])
    #update coach1 data
    team1.wins+=results['team1']['wins']
    team1.losses+=abs(results['team1']['wins']-1)
    team1.forfeit+=results['team1']['forfeit']
    if team1.forfeit == 1:
        team1.differential+=(-3)
    else:
        team1.differential+=results['team1']['score']-results['team2']['score']
    if team1.streak < 0:
        if results['team1']['wins'] == 1:
            team1.streak=1
        else:
            team1.streak+=(-1)
    else:
        if results['team1']['wins'] == 1:
            team1.streak+=1
        else:
            team1.streak=(-1)
    objectstosave.append(team1)
    #update coach2 data
    team2.wins+=results['team2']['wins']
    team2.losses+=abs(results['team2']['wins']-1)
    team2.forfeit+=results['team2']['forfeit']
    if team2.forfeit == 1:
        team2.differential+=(-3)
    else:
        team2.differential+=results['team2']['score']-results['team1']['score']
    if team2.streak < 0:
        if results['team2']['wins'] == 1:
            team2.streak=1
        else:
            team2.streak+=(-1)
    else:
        if results['team2']['wins'] == 1:
            team2.streak+=1
        else:
            team2.streak=(-1)
    objectstosave.append(team2)
    #update match
    if match.team1==team1:
        match.team1score=results['team1']['score'] 
        match.team2score=results['team2']['score'] 
        if results['team1']['wins'] ==1:
            match.winner=team1
        elif results['team2']['wins']==1:
            match.winner=team2
    elif match.team1==team2:    
        match.team1score=results['team2']['score'] 
        match.team2score=results['team1']['score'] 
        if results['team2']['wins'] ==1:
            match.winner=team2
        elif results['team1']['wins']==1:
            match.winner=team1
    objectstosave.append(match)
    if len(erroritems)==0:
        for obj in objectstosave:
            obj.save()
        messages.success(request,'Replay has been saved!')
        discordserver=subleague.discord_settings.discordserver
        discordchannel=subleague.discord_settings.replaychannel
        title=f"Week: {match.week}. {match.team1.teamname} vs {match.team2.teamname}: {match.replay}."
        replay_announcements.objects.create(
            league = discordserver,
            league_name = subleague.league.name,
            text = title,
            replaychannel = discordchannel
        )
        matchpickems=pickems.objects.all().filter(match=match)
        for item in matchpickems:
            if item.pick==match.winner:
                item.correct=True
                item.save()
    else:
        for obj in erroritems:
            messages.error(request,f'A roster spot matching {obj} does not exist.',extra_tags="danger")
    return

def pokemonsearch(pokemon,rosterofinterest,errormons):
    try:
        mon=rosterofinterest.get(pokemon__pokemon=pokemon)
    except:
        try:
            mon=rosterofinterest.get(pokemon__pokemon__icontains=pokemon)
        except:
            mon=None
            errormons.append(pokemon)
    return mon, errormons

@check_if_subleague
@check_if_season
@check_if_match
def league_match_results(request,league_name,subleague_name,matchid):
    league_name=league_name.replace('%20',' ')
    subleague=league_subleague.objects.filter(league__name=league_name).get(subleague=subleague_name)
    league_teams=subleague.subleague_coachs.all().order_by('teamname')
    match=schedule.objects.get(pk=matchid)
    if match.replay == "Link":
        messages.error(request,f'A replay for that match does not exist!',extra_tags="danger")
        return redirect('league_schedule',league_name=league_name,subleague_name=subleague.subleague)
    try:
        manualreplay=manual_replay.objects.get(match=match)
        showreplay=False
        if manualreplay.replay.find('replay.pokemonshowdown.com') >-1:
            showreplay=True
        if manualreplay.match.team1==manualreplay.winner:
            loser=manualreplay.match.team2
        if manualreplay.match.team2==manualreplay.winner:
            loser=manualreplay.match.team1
        team1score=manualreplay.match.team1score
        team2score=manualreplay.match.team2score
        score=f'{max(team1score,team2score)}-0'
        context={
            'manualreplay':manualreplay,
            'showreplay': showreplay,
            'loser': loser,
            'score': score,
            'league_teams': league_teams,
            'league_name':league_name,
            'subleague': subleague,
            'leaguepage': True,
        }
        return render(request,"manualreplayresults.html",context)
    except:
        try:
            results = match.match_replay.data
            context={
                    'results': results,
                    'league_teams': league_teams,
                    'league_name':league_name,
                    'subleague': subleague,
                    'leaguepage': True,
            }
        except:
            url=match.replay
            try:    
                results = newreplayparse(url)
            except Exception as e:
                inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url)
                messages.error(request,f'There was an error processing your replay. claduva has been notified.',extra_tags="danger")
            if len(results['errormessage'])!=0:
                inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url)
        context={
            'results': results,
            'league_teams': league_teams,
            'league_name':league_name,
            'subleague': subleague,
            'leaguepage': True,
        }
        return render(request,"replayanalysisresults.html",context)

@check_if_clad
def upload_historic_match(request):
    if request.method=="POST":
        form = UploadHistoricMatchForm(request.POST)
        league_ = request.POST['league_']
        seasonname = request.POST['seasonname']
        team1=request.POST['team1']
        team2=request.POST['team2']
        winner=request.POST['winner']
        week=request.POST['week']
        replay=request.POST['replay']
        #analyze replay
        try:
            data = newreplayparse(replay)
            if len(data['errormessage'])>0:
                messages.error(request,f'Analysis Failed.',extra_tags="danger")
            else:
                team1=historical_team.objects.filter(league=league_,seasonname=seasonname).get(teamname=team1)
                team2=historical_team.objects.filter(league=league_,seasonname=seasonname).get(teamname=team2)
                winner=historical_team.objects.filter(league=league_,seasonname=seasonname).get(teamname=winner)
                match=historical_match.objects.create(id=historical_match.objects.all().order_by('-id').first().id+1,week=week,team1=team1,team2=team2,winner=winner,replay=replay)
                success=check_hist_match(match)
                if success:
                    results = newreplayparse(replay)
                    if match.winner==match.team1:
                        match.team1score=max(results['team1']['score'],results['team2']['score'])
                    elif match.winner==match.team2:
                        match.team2score=max(results['team1']['score'],results['team2']['score'])
                    match.save()
                    messages.success(request,"Success!")    
                else:
                    messages.error(request,f'Analysis Failed.',extra_tags="danger")
        except Exception as e:
            messages.error(request,f'Analysis Failed.',extra_tags="danger")
        return redirect('upload_historic_match')
    form=UploadHistoricMatchForm()
    context={
        'form': form,
        'submission': True,
    }
    return  render(request,"replayanalysisform.html",context)

@csrf_exempt
def uploadhistoricrender(request):
    purpose=request.POST['purpose']
    if purpose=="Add Seasons":
        league_id=request.POST['associatedleague']
        league_=league.objects.get(id=league_id)
        seasons=list(historical_team.objects.filter(league=league_).order_by('seasonname').distinct('seasonname').values_list('seasonname',flat=True))
        data={
            'seasons':seasons,
            }
    elif purpose=="Add Teams":
        league_id=request.POST['associatedleague']
        seasonname=request.POST['seasonname']
        league_=league.objects.get(id=league_id)
        teams=list(historical_team.objects.filter(league=league_,seasonname=seasonname).order_by('teamname').values_list('teamname',flat=True))
        data={
            'teams':teams,
            }
    return JsonResponse(data)


@check_if_clad
def check_existing_replay(request):
    if request.method=="POST":
        form = MatchReplayForm(request.POST)
        if form.is_valid():
            url=form.cleaned_data['url']
            #currentmatch
            try:
                item=schedule.objects.get(replay=url)
                success=check_current_match(item)
                if success:
                    messages.success(request,"Match has been executed!")
            #historic match
            except:
                try:
                    item=historical_match.objects.get(replay=url)
                    success=check_hist_match(item)
                    if success:
                        messages.success(request,"Match has been executed!")
                except:
                    messages.error(request,f'Replay is not in the library.',extra_tags="danger")
    form=MatchReplayForm()
    context={
        'form': form,
        'submission': True,
    }
    return  render(request,"replayanalysisform.html",context)

@check_if_clad
def check_if_passes(request):
    currentmatches=schedule.objects.all().filter(Q(replay__contains="replay.pokemonshowdown.com")|Q(replay__contains="/static/logfiles/"))
    histmatches=historical_match.objects.all().filter(Q(replay__contains="replay.pokemonshowdown.com")|Q(replay__contains="/static/logfiles/"))
    total=currentmatches.count()+histmatches.count()
    i=1
    failed=[]
    for item in currentmatches:
        try:    
            results = newreplayparse(item.replay)
            if len(results['errormessage'])>0:
                failed.append(item.replay)
            else:
                data=item.match_replay
                data.data=results
                data.save()
        except:
            failed.append(item.replay)
        print(f'{i}/{total}')
        i+=1
    for item in histmatches:
        try:    
            results = newreplayparse(item.replay)
            if len(results['errormessage'])>0:
                failed.append(item.replay)
            else:
                data=item.historical_match_replay
                data.data=results
                data.save()
        except:
            failed.append(item.replay)
        print(f'{i}/{total}')
        i+=1
    for item in failed:
        print(item)
    return redirect('home')

@check_if_clad
def check_analyzer(request):
    check_analyzer_task()
    return redirect('home')
    
@csrf_exempt
#def check_current_match(request):
def check_current_match(match):
    #match=schedule.objects.get(id=request.POST['matchid'])
    url=match.replay
    try:
        results = newreplayparse(url)
        success=True
        if len(results['errormessage'])!=0:
            success=False
    except:
        success=False
    if success:
        try:
            mr=match.match_replay
            mr.data=results
            mr.save()
        except:
            mr=match_replay.objects.create(match=match,data=results)
        data=mr.data
        #align coachs
        winner=match.winner
        team1=match.team1
        team2=match.team2
        if (team1==winner and data['team2']['wins']>0) or (team2==winner and data['team1']['wins']>0):
            team1=match.team2
            team2=match.team1
        #update teams
        team1.wins+=data['team1']['wins']; team1.losses+=abs(data['team1']['wins']-1); team1.differential+=data['team1']['score']-data['team2']['score']; team1.forfeit=data['team1']['forfeit']
        team2.wins+=data['team2']['wins']; team2.losses+=abs(data['team2']['wins']-1); team2.differential+=data['team2']['score']-data['team1']['score']; team2.forfeit=data['team2']['forfeit']
        ##
        for mon in data['team1']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            foundmon=current_searchmon(team1,searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+=mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team1']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team1.support+=mon['support']; team1.damagedone+=mon['damagedone']; team1.hphealed+=mon['hphealed']; team1.luck+=mon['luck']; team1.remaininghealth+=mon['remaininghealth']
            foundmon.save()
            #iterate through moves
            iterate_moves(mon['moves'],team1,foundmon,url)
        for mon in data['team2']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            foundmon=current_searchmon(team2,searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+=mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team2']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team2.support+=mon['support']; team2.damagedone+=mon['damagedone']; team2.hphealed+=mon['hphealed']; team2.luck+=mon['luck']; team2.remaininghealth+=mon['remaininghealth']
            foundmon.save()
            #iterate through moves
            iterate_moves(mon['moves'],team2,foundmon,url)
        team1.save()
        team2.save()
    return success

def check_hist_match(match):    
    #match=historical_match.objects.get(id=request.POST['matchid'])
    url=match.replay
    try:
        results = newreplayparse(url)
        success=True
        if len(results['errormessage'])!=0:
            success=False
    except:
        success=False
    if success:
        try:
            mr=match.historical_match_replay
            mr.data=results
            mr.save()
        except:
            mr=historical_match_replay.objects.create(match=match,data=results)
        data=mr.data
        #align coachs
        winner=match.winner
        team1=match.team1
        team2=match.team2
        if (team1==winner and data['team2']['wins']>0) or (team2==winner and data['team1']['wins']>0):
            team1=match.team2
            team2=match.team1
        #update teams
        team1.wins+=data['team1']['wins']; team1.losses+=abs(data['team1']['wins']-1); team1.differential+=data['team1']['score']-data['team2']['score']; team1.forfeit=data['team1']['forfeit']
        team2.wins+=data['team2']['wins']; team2.losses+=abs(data['team2']['wins']-1); team2.differential+=data['team2']['score']-data['team1']['score']; team2.forfeit=data['team2']['forfeit']
        ##
        for mon in data['team1']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            foundmon=historic_searchmon(team1,searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+= mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team1']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team1.support+=mon['support']; team1.damagedone+=mon['damagedone']; team1.hphealed+=mon['hphealed']; team1.luck+=mon['luck']; team1.remaininghealth+=mon['remaininghealth']
            foundmon.save()
            #iterate through moves
            iterate_moves(mon['moves'],team1,foundmon,url)
        for mon in data['team2']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            foundmon=historic_searchmon(team2,searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+= mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team2']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team2.support+=mon['support']; team2.damagedone+=mon['damagedone']; team2.hphealed+=mon['hphealed']; team2.luck+=mon['luck']; team2.remaininghealth+=mon['remaininghealth']
            foundmon.save()
            #iterate through moves
            iterate_moves(mon['moves'],team2,foundmon,url)
        team1.save()
        team2.save()
    return success

def iterate_moves(movelist,team,foundmon,replay):
    for move in movelist:
        ##update moveinfo
        move_=move.replace("Z-","")
        moi=moveinfo.objects.get(name=move_)
        moi.uses+=movelist[move]['uses']
        moi.hits+=movelist[move]['hits']
        moi.crits+=movelist[move]['crits']
        moi.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
        moi.secondaryeffects+=movelist[move]['secondaryeffects']
        moi.save()
        ##update coach 
        #if current
        try:
            #for coach
            try:
                um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.coach)
            except:
                um=user_movedata.objects.create(moveinfo=moi,coach=team.coach)
            um.uses+=movelist[move]['uses']
            um.hits+=movelist[move]['hits']
            um.crits+=movelist[move]['crits']
            um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
            um.secondaryeffects+=movelist[move]['secondaryeffects']
            um.save()
            #for teammate
            if team.teammate:
                try:
                    um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.teammate)
                except:
                    um=user_movedata.objects.create(moveinfo=moi,coach=team.teammate)
                um.uses+=movelist[move]['uses']
                um.hits+=movelist[move]['hits']
                um.crits+=movelist[move]['crits']
                um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                um.secondaryeffects+=movelist[move]['secondaryeffects']
                um.save()
        except:
            #for coach
            try:
                um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.coach1)
            except:
                um=user_movedata.objects.create(moveinfo=moi,coach=team.coach1)
            um.uses+=movelist[move]['uses']
            um.hits+=movelist[move]['hits']
            um.crits+=movelist[move]['crits']
            um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
            um.secondaryeffects+=movelist[move]['secondaryeffects']
            um.save()
            #for teammate
            if team.coach2:
                try:
                    um=user_movedata.objects.filter(moveinfo=moi).get(coach=team.coach2)
                except:
                    um=user_movedata.objects.create(moveinfo=moi,coach=team.coach2)
                um.uses+=movelist[move]['uses']
                um.hits+=movelist[move]['hits']
                um.crits+=movelist[move]['crits']
                um.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                um.secondaryeffects+=movelist[move]['secondaryeffects']
                um.save()
        ##update mon moves
        try:
            try:
                pm=pokemon_movedata.objects.filter(moveinfo=moi).get(pokemon=foundmon)
            except:
                pm=pokemon_movedata.objects.create(moveinfo=moi,pokemon=foundmon)
            if move in list(foundmon.moves.all().values_list('moveinfo__name',flat=True)):
                pm.uses+=movelist[move]['uses']
                pm.hits+=movelist[move]['hits']
                pm.crits+=movelist[move]['crits']
                pm.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                pm.secondaryeffects+=movelist[move]['secondaryeffects']
                pm.save()
            else:
                try:
                    unmatched_moves.objects.create(pokemon=foundmon,moveinfo=moi,replay=replay)
                except:
                    pass
        #elif historic or current
        except:
            try:
                pm=pokemon_movedata.objects.filter(moveinfo=moi).get(pokemon=foundmon.pokemon)
            except:
                pm=pokemon_movedata.objects.create(moveinfo=moi,pokemon=foundmon.pokemon)
            if move in list(foundmon.pokemon.moves.all().values_list('moveinfo__name',flat=True)):
                pm.uses+=movelist[move]['uses']
                pm.hits+=movelist[move]['hits']
                pm.crits+=movelist[move]['crits']
                pm.posssecondaryeffects+=movelist[move]['posssecondaryeffects']
                pm.secondaryeffects+=movelist[move]['secondaryeffects']
                pm.save()
            else:
                try:
                    unmatched_moves.objects.create(pokemon=foundmon.pokemon,moveinfo=moi,replay=replay)
                except:
                    pass
    return

def current_searchmon(toi,searchmon):
    try:
        foundmon=roster.objects.all().filter(season__subleague=toi.subleague,team=toi).get(pokemon__pokemon=searchmon)
    except:
        try:
            foundmon=roster.objects.all().filter(season__subleague=toi.subleague,team=toi).get(pokemon__pokemon__contains=searchmon)
        except:
            try:
                foundmon=roster.objects.all().filter(season__subleague=toi.subleague).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=roster.objects.all().filter(season__subleague=toi.subleague).get(pokemon__pokemon__contains=searchmon)
                except:
                    foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
    return foundmon

def historic_searchmon(toi,searchmon):
    try:
        foundmon=historical_roster.objects.all().filter(team=toi).get(pokemon__pokemon=searchmon)
    except:
        try:
            foundmon=historical_roster.objects.all().filter(team=toi).get(pokemon__pokemon__contains=searchmon)
        except:
            try:
                foundmon=historical_roster.objects.all().filter(team__seasonname=toi.seasonname,team__subseason=toi.subseason).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=historical_roster.objects.all().filter(team__seasonname=toi.seasonname,team__subseason=toi.subseason).get(pokemon__pokemon__contains=searchmon)
                except:
                    foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
    return foundmon

def update_manual_match(match,form,request):
    season=match.season
    subleague=season.subleague
    league_name=subleague.league.name
    #get teams
    team1=match.team1
    team2=match.team2
    #get pokemon
    t1pokemon1=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t1pokemon1'])
    t1pokemon2=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t1pokemon2'])
    t1pokemon3=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t1pokemon3'])
    t1pokemon4=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t1pokemon4'])
    t1pokemon5=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t1pokemon5'])
    t1pokemon6=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t1pokemon6'])
    t2pokemon1=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t2pokemon1'])
    t2pokemon2=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t2pokemon2'])
    t2pokemon3=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t2pokemon3'])
    t2pokemon4=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t2pokemon4'])
    t2pokemon5=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t2pokemon5'])
    t2pokemon6=roster.objects.filter(season=season).get(pokemon=form.cleaned_data['t2pokemon6'])
    #update match
    match.replay=form.cleaned_data['replay']
    match.team1score=6-form.cleaned_data['t1pokemon1death']-form.cleaned_data['t1pokemon2death']-form.cleaned_data['t1pokemon3death']-form.cleaned_data['t1pokemon4death']-form.cleaned_data['t1pokemon5death']-form.cleaned_data['t1pokemon6death']
    match.team2score=6-form.cleaned_data['t2pokemon1death']-form.cleaned_data['t2pokemon2death']-form.cleaned_data['t2pokemon3death']-form.cleaned_data['t2pokemon4death']-form.cleaned_data['t2pokemon5death']-form.cleaned_data['t2pokemon6death']
    #update pokemon
    t1pokemon1.kills+=form.cleaned_data['t1pokemon1kills']
    t1pokemon2.kills+=form.cleaned_data['t1pokemon2kills']
    t1pokemon3.kills+=form.cleaned_data['t1pokemon3kills']
    t1pokemon4.kills+=form.cleaned_data['t1pokemon4kills']
    t1pokemon5.kills+=form.cleaned_data['t1pokemon5kills']
    t1pokemon6.kills+=form.cleaned_data['t1pokemon6kills']
    t2pokemon1.kills+=form.cleaned_data['t2pokemon1kills']
    t2pokemon2.kills+=form.cleaned_data['t2pokemon2kills']
    t2pokemon3.kills+=form.cleaned_data['t2pokemon3kills']
    t2pokemon4.kills+=form.cleaned_data['t2pokemon4kills']
    t2pokemon5.kills+=form.cleaned_data['t2pokemon5kills']
    t2pokemon6.kills+=form.cleaned_data['t2pokemon6kills']
    t1pokemon1.deaths+=form.cleaned_data['t1pokemon1death']
    t1pokemon2.deaths+=form.cleaned_data['t1pokemon2death']
    t1pokemon3.deaths+=form.cleaned_data['t1pokemon3death']
    t1pokemon4.deaths+=form.cleaned_data['t1pokemon4death']
    t1pokemon5.deaths+=form.cleaned_data['t1pokemon5death']
    t1pokemon6.deaths+=form.cleaned_data['t1pokemon6death']
    t2pokemon1.deaths+=form.cleaned_data['t2pokemon1death']
    t2pokemon2.deaths+=form.cleaned_data['t2pokemon2death']
    t2pokemon3.deaths+=form.cleaned_data['t2pokemon3death']
    t2pokemon4.deaths+=form.cleaned_data['t2pokemon4death']
    t2pokemon5.deaths+=form.cleaned_data['t2pokemon5death']
    t2pokemon6.deaths+=form.cleaned_data['t2pokemon6death']
    t1pokemon1.differential+=form.cleaned_data['t1pokemon1kills']-form.cleaned_data['t1pokemon1death']
    t1pokemon2.differential+=form.cleaned_data['t1pokemon2kills']-form.cleaned_data['t1pokemon2death']
    t1pokemon3.differential+=form.cleaned_data['t1pokemon3kills']-form.cleaned_data['t1pokemon3death']
    t1pokemon4.differential+=form.cleaned_data['t1pokemon4kills']-form.cleaned_data['t1pokemon4death']
    t1pokemon5.differential+=form.cleaned_data['t1pokemon5kills']-form.cleaned_data['t1pokemon5death']
    t1pokemon6.differential+=form.cleaned_data['t1pokemon6kills']-form.cleaned_data['t1pokemon6death']
    t2pokemon1.differential+=form.cleaned_data['t2pokemon1kills']-form.cleaned_data['t2pokemon1death']
    t2pokemon2.differential+=form.cleaned_data['t2pokemon2kills']-form.cleaned_data['t2pokemon2death']
    t2pokemon3.differential+=form.cleaned_data['t2pokemon3kills']-form.cleaned_data['t2pokemon3death']
    t2pokemon4.differential+=form.cleaned_data['t2pokemon4kills']-form.cleaned_data['t2pokemon4death']
    t2pokemon5.differential+=form.cleaned_data['t2pokemon5kills']-form.cleaned_data['t2pokemon5death']
    t2pokemon6.differential+=form.cleaned_data['t2pokemon6kills']-form.cleaned_data['t2pokemon6death']
    t1pokemon1.gp+=1; t1pokemon2.gp+=1; t1pokemon3.gp+=1; t1pokemon4.gp+=1; t1pokemon5.gp+=1; t1pokemon6.gp+=1
    t2pokemon1.gp+=1; t2pokemon2.gp+=1; t2pokemon3.gp+=1; t2pokemon4.gp+=1; t2pokemon5.gp+=1; t2pokemon6.gp+=1
    winner=form.cleaned_data['winner']
    match.winner=winner
    if winner == match.team1:
        team1.wins+=1; team2.losses+=1
        t1pokemon1.gw+=1; t1pokemon2.gw+=1; t1pokemon3.gw+=1; t1pokemon4.gw+=1; t1pokemon5.gw+=1; t1pokemon6.gw+=1
        if team1.streak>-1:
            team1.streak+=1
        else:
            team1.streak=1
        if team2.streak>-1:
            team2.streak=(-1)
        else:
            team2.streak+=(-1)
    elif winner == match.team2:
        team2.wins+=1; team1.losses+=1
        t2pokemon1.gw+=1; t2pokemon2.gw+=1; t2pokemon3.gw+=1; t2pokemon4.gw+=1; t2pokemon5.gw+=1; t2pokemon6.gw+=1
        if team2.streak>-1:
            team2.streak+=1
        else:
            team2.streak=1
        if team1.streak>-1:
            team1.streak=(-1)
        else:
            team1.streak+=(-1)
    if match.team1score>match.team2score:
        team1.differential+=match.team1score
    elif match.team2score>match.team1score:
        team1.differential+=(-match.team2score)
    if match.team2score>match.team1score:
        team2.differential+=match.team2score
    elif match.team1score>match.team2score:
        team2.differential+=(-match.team1score)
    #save data
    data=form.save(); match.save(); team1.save(); team2.save()
    t1pokemon1.save(); t1pokemon2.save(); t1pokemon3.save(); t1pokemon4.save(); t1pokemon5.save(); t1pokemon6.save()
    t2pokemon1.save(); t2pokemon2.save(); t2pokemon3.save(); t2pokemon4.save(); t2pokemon5.save(); t2pokemon6.save()
    messages.success(request,"Match has been saved!")
    discordserver=subleague.discord_settings.discordserver
    discordchannel=subleague.discord_settings.replaychannel
    title=f"Week: {match.week}. {match.team1.teamname} vs {match.team2.teamname}: {match.replay}."
    replay_announcements.objects.create(
        league = discordserver,
        league_name = league_name,
        text = title,
        replaychannel = discordchannel
    )
    return data

def render_uploaded_replay(request,string):
    context={}
    return  render(request,string+".html",context)

##--------------------------------------------TASKS--------------------------------------------
@background(schedule=1)
def check_analyzer_task():
    print("TASK: Running check analyzer")
    ##zero rosters  
    roster.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    historical_roster.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    all_pokemon.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    ##zero coachs
    coachdata.objects.all().update(wins=0,losses=0,differential=0,forfeit=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    historical_team.objects.all().update(wins=0,losses=0,differential=0,forfeit=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    ##zero movedata
    moveinfo.objects.all().update(uses=0,hits=0,crits=0,posssecondaryeffects=0,secondaryeffects=0)
    pokemon_movedata.objects.all().update(uses=0,hits=0,crits=0,posssecondaryeffects=0,secondaryeffects=0)
    user_movedata.objects.all().update(uses=0,hits=0,crits=0,posssecondaryeffects=0,secondaryeffects=0)
    ##get matches
    failed_replay.objects.all().delete()
    currentmatches=schedule.objects.all().filter(Q(replay__contains="replay.pokemonshowdown.com")|Q(replay__contains="/static/logfiles/"))
    histmatches=historical_match.objects.all().filter(Q(replay__contains="replay.pokemonshowdown.com")|Q(replay__contains="/static/logfiles/"))
    histffmatches=historical_match.objects.all().filter(replay__contains="Forfeit").order_by('id')
    ffmatches=schedule.objects.all().filter(replay__contains="Forfeit").order_by('id')
    unavailable=historical_match.objects.all().filter(replay="Unavailable")
    total=currentmatches.count()+histmatches.count()+histffmatches.count()+ffmatches.count()+unavailable.count()
    i=1
    failed=[]
    print('Current')
    for item in currentmatches:
        try:
            success=check_current_match(item)
            if not success:
                failed.append(item)
                print(f'{item.id}: {item.replay}')
        except:
            failed.append(item)
            print(f'{item.id}: {item.replay}')
        print(f'{i}/{total}')
        i+=1
    print('Historic')
    for item in histmatches:
        try:
            success=check_hist_match(item)
            if not success:
                failed.append(item)
                print(f'{item.id}: {item.replay}')
        except:
            failed.append(item)
            print(f'{item.id}: {item.replay}')
        print(f'{i}/{total}')
        i+=1
    #forfeits
    print('Forfeit')
    for item in ffmatches:
        team1=item.team1
        team2=item.team2
        if item.replay=="Both Teams Forfeit":
            team1.differential+=-3
            team2.differential+=-3
            team1.losses+=1
            team2.losses+=1
            team1.forfeit+=1
            team2.forfeit+=1
        elif item.replay=="Team 1 Forfeits":
            team1.differential+=-3
            team2.differential+=3
            team1.losses+=1
            team2.wins+=1
            team1.forfeit+=1
        elif item.replay=="Team 2 Forfeits":
            team2.differential+=-3
            team1.differential+=3
            team2.losses+=1
            team1.wins+=1
            team2.forfeit+=1
        team1.save()
        team2.save()
        print(f'{i}/{total}')
        i+=1
    for item in histffmatches:
        team1=item.team1
        team2=item.team2
        if item.replay=="Both Teams Forfeit":
            team1.differential+=-3
            team2.differential+=-3
            team1.losses+=1
            team2.losses+=1
            team1.forfeit+=1
            team2.forfeit+=1
        elif item.replay=="Team 1 Forfeits":
            team1.differential+=-3
            team2.differential+=3
            team1.losses+=1
            team2.wins+=1
            team1.forfeit+=1
        elif item.replay=="Team 2 Forfeits":
            team2.differential+=-3
            team1.differential+=3
            team2.losses+=1
            team1.wins+=1
            team2.forfeit+=1
        team1.save()
        team2.save()
        print(f'{i}/{total}')
        i+=1
    #unavailable
    print('Unavailable')
    for item in unavailable:
        team1=item.team1
        team2=item.team2
        team1.differential+=item.team1score-item.team2score
        team2.differential+=item.team2score-item.team1score
        if item.winner==item.team1:
            team1.wins+=1
            team2.losses+=1
        elif item.winner==item.team2:
            team2.wins+=1
            team1.losses+=1
        print(f'{i}/{total}')
        i+=1
    print('Failed')
    for item in failed:
        failed_replay.objects.create(replay=item.replay)
        print(f'{item.id}: {item.replay}')