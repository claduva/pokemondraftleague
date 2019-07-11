def runscript(request):
    ##trading
    historical_trading.objects.all().delete()
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
    historical_freeagency.objects.all().delete()
    with open('freeagency.csv') as csv_file:
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
                historical_freeagency.objects.create(
                    team=team_,
                    addedpokemon=addedpokemon_,
                    droppedpokemon=droppedpokemon_
                )
                line_count += 1
    
    ##roster
    historical_roster.objects.all().delete()
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
    historical_draft.objects.all().delete()
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
    historical_team.objects.all().delete()
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