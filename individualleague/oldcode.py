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
        except Exception as e:
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