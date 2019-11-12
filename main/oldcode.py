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
                replay=row[9]
                try:
                    winner=historical_team.objects.get(id=row[6])
                except:
                    winner=None
                try:    
                    results = newreplayparse(replay)
                    team1score= results['team1']['score']
                    team2score= results['team2']['score']
                except:
                    team1score=0
                    team2score=0
                #create match
                moi=historical_match.objects.create(week=week,team1=team1,team2=team2,winner=winner,team1score=team1score,team2score=team2score,replay=replay)
                try:
                    historical_match_replay.objects.create(match=moi,data=results)
                except: 
                    pass
                line_count += 1
                print(line_count)
                print(replay)
    ##effectiveness calc
    ap=all_pokemon.objects.all()
    j=1
    for i in ap:
        print(j)
        typing=i.types.all()
        i=i.effectiveness
        for t in typing:
            if t.typing=="Bug":
                i.fighting+=1
                i.flying+=-1
                i.ground+=1
                i.rock+=-1
                i.fire+=-1
                i.grass+=1
            elif t.typing=="Dark":
                i.fighting+=-1
                i.bug+=-1
                i.ghost+=1
                i.dark+=1
                i.fairy+=-1
            elif t.typing=="Dragon":
                i.fire+=1
                i.water+=1
                i.grass+=1
                i.electric+=1
                i.ice+=-1
                i.dragon+=-1
                i.fairy+=-1
            elif t.typing=="Electric":
                i.flying+=1
                i.ground+=-1
                i.steel+=1
                i.electric+=1
            elif t.typing=="Fairy":
                i.fighting+=1
                i.poison+=-1
                i.bug+=1
                i.steel+=-1
                i.dark+=1
            elif t.typing=="Fighting":
                i.flying+=-1
                i.rock+=1
                i.bug+=1
                i.psychic+=-1
                i.dark+=1
                i.fairy+=-1
            elif t.typing=="Fire":
                i.ground+=-1
                i.rock+=-1
                i.bug+=1
                i.steel+=1
                i.fire+=1
                i.water+=-1
                i.grass+=1
                i.ice+=1
                i.fairy+=1
            elif t.typing=="Flying":
                i.fighting+=1
                i.rock+=-1
                i.bug+=1
                i.grass+=1
                i.electric+=-1
                i.ice+=-1
            elif t.typing=="Ghost":
                i.poison+=1
                i.bug+=1
                i.dark+=-1
                i.ghost+=-1
            elif t.typing=="Grass":
                i.flying+=-1
                i.poison+=-1
                i.grass+=1
                i.ground+=1
                i.bug+=-1
                i.fire+=-1
                i.water+=1
                i.electric+=1
                i.ice+=-1
            elif t.typing=="Ground":
                i.poison+=1
                i.rock+=1
                i.water+=-1
                i.grass+=-1
                i.ice+=-1
            elif t.typing=="Ice":
                i.fighting+=1
                i.steel+=1
                i.fire+=1
                i.rock+=1
                i.ice+=-1
            elif t.typing=="Normal":
                i.fighting+=-1
            elif t.typing=="Poison":
                i.fighting+=1
                i.poison+=1
                i.ground+=-1
                i.bug+=1
                i.grass+=1
                i.psychic+=-1
                i.fairy+=1
            elif t.typing=="Psychic":
                i.fighting+=1
                i.bug+=-1
                i.ghost+=-1
                i.dark+=-1
                i.psychic+=1
            elif t.typing=="Rock":
                i.normal+=1
                i.fighting+=-1
                i.flying+=1
                i.poison+=1
                i.ground+=-1
                i.steel+=1
                i.fire+=1
                i.water+=-1
                i.grass+=-1
            elif t.typing=="Steel":
                i.normal+=1
                i.fighting+=-1
                i.flying+=1
                i.ground+=-1
                i.rock+=1
                i.bug+=1
                i.steel+=1
                i.fire+=-1
                i.grass+=1
                i.psychic+=1
                i.ice+=1
                i.dragon+=1
                i.fairy+=1
            elif t.typing=="Water":
                i.steel+=1
                i.fire+=1
                i.water+=1
                i.grass+=-1
                i.electric=-1
                i.ice+=1
            else:
                print(t.typing)
        i.save()
        j+=1
    return redirect('home')