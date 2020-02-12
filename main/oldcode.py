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

with open("swsh.txt") as fp:
        count=0
        mon=""
        monlist=[]
        for line in fp:
            line=line.strip()
            #find mon
            if line.find("Stage")>-1:
                mon=line.split(" - ",1)[1].split(" (Stage:")[0]
            if line.find("Base Stats")>-1:
                line_=line.replace("Base Stats: ",",").replace(" (BST: ",",").replace(")","").replace(".",",")
                mon+=line_
            if line.find("Abilities")>-1:
                line_=line.replace("Abilities: ","").replace(" (1)","").replace(" (2)","").replace(" (H)","").split(" | ")
                if line_[0]==line_[1]:
                    line_[1]="None"
                if line_[0]==line_[2]:
                    line_[2]="None"
                for a in line_:
                    mon+=","+a
            if line.find("Type: ")>-1:
                if line.find(" / ")==-1:
                    line+=",None"
                line_=line.replace("Type: ","").replace(" / ",",")
                mon+=","+line_
            #add to mon list
            if line=="======":
                count+=1
                if count%2==1 and count>1:
                    monlist.append(mon)
                    print(mon)
        #print(monlist)


#import galar mons
 with open('gen8prep.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        idoi=all_pokemon.objects.all().order_by('id').last().id
        abilityid=pokemon_ability.objects.all().order_by('id').last().id
        typingid=pokemon_type.objects.all().order_by('id').last().id
        idoi+=1
        abilityid+=1
        typingid+=1
        for row in csv_reader:
            if line_count ==0:
                line_count += 1
            else:
                try:
                    moi=all_pokemon.objects.get(pokemon=row[0])
                    moi.hp = row[3]
                    moi.attack = row[4]
                    moi.defense = row[5]
                    moi.s_attack = row[6]
                    moi.s_defense = row[7]
                    moi.speed = row[8]
                    moi.bst = row[9]
                    moi.gen8=True
                    moi.save()
                except:
                    moi=all_pokemon.objects.create(id=idoi,pokemon=row[0],hp = row[3],attack = row[4],defense = row[5],s_attack = row[6],s_defense = row[7],speed = row[8],bst = row[9],is_fully_evolved = True,nicknames=[],gen8=True)
                    idoi+=1
                    pokemon_ability.objects.create(id=abilityid,pokemon=moi,ability=row[10])
                    abilityid+=1
                    if row[11] != "None":
                        pokemon_ability.objects.create(id=abilityid,pokemon=moi,ability=row[11])
                        abilityid+=1
                    if row[12] != "None":
                        pokemon_ability.objects.create(id=abilityid,pokemon=moi,ability=row[12])
                        abilityid+=1
                    pokemon_type.objects.create(id=typingid,pokemon=moi,typing=row[13])
                    typingid+=1
                    if row[14] != "None":
                        pokemon_type.objects.create(id=typingid,pokemon=moi,typing=row[14])
                        typingid+=1
                    print(row[0])
                line_count += 1

"""
    ap=all_pokemon.objects.all()
    spritecats=[
        ['swsh','ani','standard','ani','gif'],
        ['swsh','png','standard','dex','png'],
        ['swsh','ani','shiny','ani-shiny','gif'],
        ['swsh','png','shiny','dex-shiny','png'],
        ['bw','png','standard','gen5','png'],
        ['bw','png','shiny','gen5-shiny','png'],
        ['afd','png','standard','afd','png'],
        ['afd','png','shiny','afd-shiny','png'],
    ]
    for item in ap:
        for cat in spritecats:
            spritename=item.pokemon.lower().replace(" ","").replace(".","").replace("%","").replace(":","").replace("-","").replace("mega-","mega").replace("nidoran-m","nidoran").replace("o-o","oo").replace("dusk-mane","duskmane").replace("dawn-wings","dawnwings")
            url=f"https://play.pokemonshowdown.com/sprites/{cat[3]}/{spritename}.{cat[4]}"
            resp = requests.get(url)
            if resp.ok:
                resp=resp.content
                open(f'sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'wb').write(resp)
                """

ap=all_pokemon.objects.all()
    for item in ap:
        sprites=item.sprite
        print(item.pokemon)
        failed=[]
        cat=['afd','png','standard','afd','png']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.afd.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])
        cat=['afd','png','shiny','afd-shiny','png']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.afdshiny.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])
        cat=['bw','png','standard','gen5','png']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.bw.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])
        cat=['bw','png','shiny','gen5-shiny','png']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.bwshiny.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])
        cat=['swsh','ani','standard','ani','gif']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.dexani.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])
        cat=['swsh','png','standard','dex','png']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.dex.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])
        cat=['swsh','ani','shiny','ani-shiny','gif']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.dexanishiny.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])
        cat=['swsh','png','shiny','dex-shiny','png']
        try:
            with open(f'pokemondatabase/static/pokemondatabase/sprites/{cat[0]}/{cat[1]}/{cat[2]}/{item.pokemon}.{cat[4]}'.replace(":",""), 'rb') as img:
                data=img.read()
            sprites.dexshiny.save(f'{item.pokemon}.{cat[4]}'.replace(":",""), ContentFile(data))
        except:
            failed.append([item.pokemon,cat[3],cat[1]])