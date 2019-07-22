def runscript(request):
    ##trading
    with open('trading.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count ==0:
                line_count += 1
            else:
                teamid=row[1]
                addedpokemon_=row[3]
                droppedpokemon_=row[4]
                team_=historical_team.objects.get(id=teamid)
                addedpokemon_=all_pokemon.objects.get(pokemon=addedpokemon_)
                droppedpokemon_=all_pokemon.objects.get(pokemon=droppedpokemon_)
                historical_trading.objects.create(
                    team=team_,
                    addedpokemon=addedpokemon_,
                    droppedpokemon=droppedpokemon_
                )
                line_count += 1
    
    ##free agency
    with open('freeagency.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count ==0:
                line_count += 1
            else:
                teamid=row[1]
                addedpokemon_=row[4]
                droppedpokemon_=row[3]
                team_=historical_team.objects.get(id=teamid)
                addedpokemon_=all_pokemon.objects.get(pokemon=addedpokemon_)
                droppedpokemon_=all_pokemon.objects.get(pokemon=droppedpokemon_)
                historical_freeagency.objects.create(
                    team=team_,
                    addedpokemon=addedpokemon_,
                    droppedpokemon=droppedpokemon_
                )
                line_count += 1
    
    ##roster
    with open('roster.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count ==0:
                line_count += 1
            else:
                teamid=row[1]
                pokemon_=row[3]
                print(f'{pokemon_}')
                team_=historical_team.objects.get(id=teamid)
                pokemon_=all_pokemon.objects.get(pokemon=pokemon_)
                historical_roster.objects.create(
                    team=team_,
                    pokemon=pokemon_,
                )
                line_count += 1
                
    ##draft
    with open('draft.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                teamid=row[1]
                picknumber_=row[2]
                pokemon_=row[4]
                team_=historical_team.objects.get(id=teamid)
                pokemon_=all_pokemon.objects.get(pokemon=pokemon_)
                historical_draft.objects.create(
                    team=team_,
                    pokemon=pokemon_,
                    picknumber=picknumber_
                )
                line_count += 1
            print(f'{line_count}')
    ##historical teams
    with open('teams.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                teamid=row[0]
                leaguename=row[1]
                seasonname_=row[2]
                teamname_=row[3]
                coachusername=row[6]
                coachname=row[5]
                teammateusername=row[8]
                teammatename=row[7]
                logolink=row[9]
                leaguetoadd=league.objects.get(name=leaguename)
                coach1_=User.objects.get(username=coachusername)
                if teammatename == "":
                    coach2_=None
                    coach2username_=None
                else:
                    coach2_=User.objects.get(username=teammateusername)
                    coach2username_=teammatename
                addedteam=historical_team.objects.create(
                    id=teamid,
                    league = leaguetoadd,
                    seasonname = seasonname_,
                    teamname = teamname_,
                    coach1= coach1_,
                    coach1username=coachname, 
                    coach2= coach2_,
                    coach2username= coach2username_
                    )
                if logolink!="":
                    r = requests.get(logolink)
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(r.content)
                    img_temp.flush()
                    addedteam.logo.save(f"{teamname_}_{seasonname_}.png", File(img_temp), save=True)
                print(f'{teamid}')
        
##update historical teams
    with open('teams.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                teamid=row[0]
                coachname=row[5]
                itemtomodify=historical_team.objects.get(id=teamid)
                print(itemtomodify)
                itemtomodify.coach1username=coachname
                itemtomodify.save()
                print(f'{teamid}')

#match analysis
    with open('match.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count ==0:
                line_count += 1
                print(line_count)
            else:
                week=row[1]
                team1=historical_team.objects.get(id=row[2])
                team2=historical_team.objects.get(id=row[4])
                score=row[8]
                replay=row[9]
                t1ff=int(row[10])
                t2ff=int(row[11])
                try:
                    winner=historical_team.objects.get(id=row[6])
                except:
                    winner=None
                if replay != "":
                    outputstring, team1_, team2_ = replayparse(replay)
                    if team1_.win==1 and winner==team2:
                        team1__=team1
                        team2__=team2
                        team1=team2__
                        team2=team1__
                    elif team2_.win==1 and winner==team1:
                        team1__=team1
                        team2__=team2
                        team1=team2__
                        team2=team1__
                    #create match
                    historical_match.objects.create(week=week,team1=team1,team2=team2,winner=winner,team1score=team1_.score,team2score=team2_.score,replay=replay)
                    #update teams
                    team1.wins+=team1_.win
                    team1.losses+=abs(team1_.win-1)
                    team1.differential+=team1_.diff
                    team1.forfeit+=team1_.forfeit
                    team2.wins+=team2_.win
                    team2.losses+=abs(team2_.win-1)
                    team2.differential+=team2_.diff
                    team2.forfeit+=team2_.forfeit
                    #update pokemon
                    item=findpoke(team1,team2,team1_.pokemon1,line_count)
                    item.kills+=team1_.P1K
                    item.deaths+=team1_.P1F
                    item.differential+=team1_.P1Diff
                    item.gp+=1
                    item.gw+=team1_.win
                    item.save()
                    item=findpoke(team1,team2,team1_.pokemon2,line_count)
                    item.kills+=team1_.P2K
                    item.deaths+=team1_.P2F
                    item.differential+=team1_.P2Diff
                    item.gp+=1
                    item.gw+=team1_.win
                    item.save()
                    item=findpoke(team1,team2,team1_.pokemon3,line_count)
                    item.kills+=team1_.P3K
                    item.deaths+=team1_.P3F
                    item.differential+=team1_.P3Diff
                    item.gp+=1
                    item.gw+=team1_.win
                    item.save()
                    item=findpoke(team1,team2,team1_.pokemon4,line_count)
                    item.kills+=team1_.P4K
                    item.deaths+=team1_.P4F
                    item.differential+=team1_.P4Diff
                    item.gp+=1
                    item.gw+=team1_.win
                    item.save()
                    item=findpoke(team1,team2,team1_.pokemon5,line_count)
                    item.kills+=team1_.P5K
                    item.deaths+=team1_.P5F
                    item.differential+=team1_.P5Diff
                    item.gp+=1
                    item.gw+=team1_.win
                    item.save()
                    item=findpoke(team1,team2,team1_.pokemon6,line_count)
                    item.kills+=team1_.P6K
                    item.deaths+=team1_.P6F
                    item.differential+=team1_.P6Diff
                    item.gp+=1
                    item.gw+=team1_.win
                    item.save()
                    item=findpoke(team2,team1,team2_.pokemon1,line_count)
                    item.kills+=team2_.P1K
                    item.deaths+=team2_.P1F
                    item.differential+=team2_.P1Diff
                    item.gp+=1
                    item.gw+=team2_.win
                    item.save()
                    item=findpoke(team2,team1,team2_.pokemon2,line_count)
                    item.kills+=team2_.P2K
                    item.deaths+=team2_.P2F
                    item.differential+=team2_.P2Diff
                    item.gp+=1
                    item.gw+=team2_.win
                    item.save()
                    item=findpoke(team2,team1,team2_.pokemon3,line_count)
                    item.kills+=team2_.P3K
                    item.deaths+=team2_.P3F
                    item.differential+=team2_.P3Diff
                    item.gp+=1
                    item.gw+=team2_.win
                    item.save()
                    item=findpoke(team2,team1,team2_.pokemon4,line_count)
                    item.kills+=team2_.P4K
                    item.deaths+=team2_.P4F
                    item.differential+=team2_.P4Diff
                    item.gp+=1
                    item.gw+=team2_.win
                    item.save()
                    item=findpoke(team2,team1,team2_.pokemon5,line_count)
                    item.kills+=team2_.P5K
                    item.deaths+=team2_.P5F
                    item.differential+=team2_.P5Diff
                    item.gp+=1
                    item.gw+=team2_.win
                    item.save()
                    item=findpoke(team2,team1,team2_.pokemon6,line_count)
                    item.kills+=team2_.P6K
                    item.deaths+=team2_.P6F
                    item.differential+=team2_.P6Diff
                    item.gp+=1
                    item.gw+=team2_.win
                    item.save()
                else:
                    if team1==winner and t2ff==0:
                        team1score=int(score)
                        team2score=0
                        team1.wins+=1
                        team2.losses+=1
                        team1.differential+=int(score)
                        team2.differential+=(-int(score))
                    elif team2==winner and t1ff==0:
                        team1score=0
                        team2score=int(score)
                        team2.wins+=1
                        team1.losses+=1
                        team2.differential+=int(score)
                        team1.differential+=(-int(score))
                    elif team1==winner and t2ff==1:
                        team1score=3
                        team2score=0
                        team1.wins+=1
                        team2.losses+=1
                        team2.differential+=-6
                        team1.differential+=3
                        replay="T2FF"
                    elif team2==winner and t1ff==1:
                        team1score=0
                        team2score=3
                        team2.wins+=1
                        team1.losses+=1
                        team2.differential+=3
                        team1.differential+=-6
                        replay="T1FF"
                    elif t1ff==1 and t2ff==1:
                        team1score=0
                        team2score=0
                        team2.losses+=1
                        team1.losses+=1
                        team2.differential+=-6
                        team1.differential+=-6
                        replay="BothFF"
                    team1.forfeit+=t1ff
                    team2.forfeit+=t2ff
                    #create match
                    historical_match.objects.create(week=week,team1=team1,team2=team2,winner=winner,team1score=team1score,team2score=team2score,replay=replay)
                team1.save()
                team2.save()
                line_count += 1
                print(line_count)