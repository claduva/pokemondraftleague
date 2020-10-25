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
                    draftchannel=subleague.discord_settings.draftchannel
                    #send to bot
                    try:
                        upnext=draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.username
                        upnextid=str(draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.profile.discordid)
                    except:
                        upnext="The draft has concluded"
                    return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
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
                        draftchannel=subleague.discord_settings.draftchannel
                        #send to bot
                        try:
                            upnext=draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.username
                            upnextid=str(draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.profile.discordid)
                        except:
                            upnext="The draft has concluded"
                        return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
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
                return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
            searchroster=roster.objects.filter(season=season,pokemon=draftpick).first()
            if searchroster!=None:
                messages.error(request,f'{draftpick.pokemon } has already been drafted!',extra_tags='danger')
                return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
            currentpick.pokemon=draftpick
            rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
            rosterspot.pokemon=draftpick
            rosterspot.save()
            currentpick.save()
            text=f'The {currentpick.team.teamname} have drafted {draftpick.pokemon}'
            draftchannel=subleague.discord_settings.draftchannel
            #send to bot
            try:
                upnext=draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.username
                upnextid=str(draftlist.filter(pokemon__isnull=True).get(id=currentpick.id+1).team.coach.profile.discordid)
            except:
                upnext="The draft has concluded"
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
        return redirect('league_draft',league_name=league_name,subleague_name=subleague_name)
    bannedpokemon=pokemon_tier.objects.all().filter(subleague=subleague).filter(tier__tiername='Banned').values_list('pokemon',flat=True)
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
                cost=pick.pokemon.pokemon_tiers.all().get(subleague=subleague).tier.tierpoints
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