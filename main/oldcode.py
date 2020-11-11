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
ap=pokemon_effectiveness.objects.all()
ap.update(bug=0,dark=0,dragon=0,electric=0,fairy=0,fighting=0,fire=0,flying=0,ghost=0,grass=0,ground=0,ice=0,normal=0,poison=0,psychic=0,rock=0,steel=0,water=0,)
ap_=all_pokemon.objects.all()
for item in ap_:
    try:
        item.effectiveness
    except:
        pokemon_effectiveness.objects.create(pokemon=item)
j=1
for i in ap:
    print(j)
    typing=i.pokemon.types.all()
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
            i.fighting+=-1
            i.steel+=-1
            i.fire+=-1
            i.rock+=-1
            i.ice+=1
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
            i.steel+=-1
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
            i.electric+=-1
            i.ice+=1
    for t in typing:
        if t.typing=="Dark":
            i.psychic=3
        elif t.typing=="Fairy":
            i.dragon=3
        elif t.typing=="Flying":
            i.ground=3
        elif t.typing=="Ghost":
            i.normal=3
            i.fighting=3
        elif t.typing=="Ground":
            i.electric=3
        elif t.typing=="Normal":
            i.ghost=3
        elif t.typing=="Steel":
            i.poison=3
    i.save()
    j+=1

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

fs=pokemon_sprites.objects.all().filter(dex='sprites/sprite_placeholder.gif')
for item in fs:
    print(item.pokemon)
    url=f"https://play.pokemonshowdown.com/sprites/dex/{item.pokemon.pokemon.lower().replace('.','')}.png"
    resp = requests.get(url)
    if resp.ok:
        try:
            resp=resp.content
            open(f'sprites/{item.pokemon.pokemon.replace(".","")}.png', 'wb').write(resp)
            with open(f'sprites/{item.pokemon.pokemon.replace(".","")}.png', 'rb') as img:
                data=img.read()
            item.dex.save(f'{item.pokemon.pokemon.replace(".","")}.png', ContentFile(data))
        except:
            print(item.pokemon)
    else:
        print(item.pokemon)

pokemon_moveset.objects.all().delete()
allmoves=moveinfo.objects.all()
with open('learnsets.json') as json_file:
    data = json.load(json_file)
    id_=1
    for item in all_pokemon.objects.all():
        print(f'{id_}: {item.pokemon}')
        id_+=1
        name=item.pokemon.lower().replace("-mega-x","").replace("-mega-y","").replace("-mega","").replace("-gmax","").replace(" ","").replace("-","").replace("-y","").replace("-x","").replace(".","").replace(":","").replace("unbound","").replace("primal","").replace("therian","").replace("shayminsky","shaymin")
        name=name.replace('deoxysattack','deoxys').replace('deoxysdefense','deoxys').replace('deoxysspeed','deoxys').replace('origin','').replace('10%','').replace('complete','')
        try:
            ls=data[name]['learnset']
            for move in ls:
                try:
                    moi=allmoves.get(altname=move)
                    pokemon_moveset.objects.create(pokemon=item,moveinfo=moi)
                except:
                    print(move)
        except:
            pass
for item in all_pokemon.objects.all():
    data={}
    data[item.pokemon]={}
    data[item.pokemon]['basestats']={}
    data[item.pokemon]['basestats']['hp']=item.hp
    data[item.pokemon]['basestats']['attack']=item.attack
    data[item.pokemon]['basestats']['defense']=item.defense
    data[item.pokemon]['basestats']['s_attack']=item.s_attack
    data[item.pokemon]['basestats']['s_defense']=item.s_defense
    data[item.pokemon]['basestats']['speed']=item.speed
    data[item.pokemon]['basestats']['bst']=item.bst
    data[item.pokemon]['types']=[]
    for t in item.types.all():
        data[item.pokemon]['types'].append(t.typing)
    data[item.pokemon]['abilities']=[]
    for a in item.abilities.all():
        data[item.pokemon]['abilities'].append(a.ability)
    data[item.pokemon]['learnset']={}
    for move in item.moves.all():
        data[item.pokemon]['learnset'][move.moveinfo.name]={}
        data[item.pokemon]['learnset'][move.moveinfo.name]['Type']=move.moveinfo.move_typing
        data[item.pokemon]['learnset'][move.moveinfo.name]['Category']=move.moveinfo.move_category
        data[item.pokemon]['learnset'][move.moveinfo.name]['Power']=move.moveinfo.move_power
        data[item.pokemon]['learnset'][move.moveinfo.name]['Accuracy']=move.moveinfo.move_accuracy
        data[item.pokemon]['learnset'][move.moveinfo.name]['Priority']=move.moveinfo.move_priority
        data[item.pokemon]['learnset'][move.moveinfo.name]['Secondary Effect']=move.moveinfo.secondary_effect
        data[item.pokemon]['learnset'][move.moveinfo.name]['Secondary Effect Chance']=move.moveinfo.secondary_effect_chance
    data[item.pokemon]['typematchup']={}
    effectiveness=item.effectiveness
    data[item.pokemon]['typematchup']['Bug']=effectiveness.bug
    data[item.pokemon]['typematchup']['Dark']=effectiveness.dark
    data[item.pokemon]['typematchup']['Dragon']=effectiveness.dragon
    data[item.pokemon]['typematchup']['Electric']=effectiveness.electric
    data[item.pokemon]['typematchup']['Fairy']=effectiveness.fairy
    data[item.pokemon]['typematchup']['Fighting']=effectiveness.fighting
    data[item.pokemon]['typematchup']['Fire']=effectiveness.fire
    data[item.pokemon]['typematchup']['Flying']=effectiveness.flying
    data[item.pokemon]['typematchup']['Ghost']=effectiveness.ghost
    data[item.pokemon]['typematchup']['Grass']=effectiveness.grass
    data[item.pokemon]['typematchup']['Ground']=effectiveness.ground
    data[item.pokemon]['typematchup']['Ice']=effectiveness.ice
    data[item.pokemon]['typematchup']['Normal']=effectiveness.normal
    data[item.pokemon]['typematchup']['Poison']=effectiveness.poison
    data[item.pokemon]['typematchup']['Psychic']=effectiveness.psychic
    data[item.pokemon]['typematchup']['Rock']=effectiveness.rock
    data[item.pokemon]['typematchup']['Steel']=effectiveness.steel
    data[item.pokemon]['typematchup']['Water']=effectiveness.water
    data[item.pokemon]['sprites']={}
    sprites=item.sprite
    data[item.pokemon]['sprites']["swsh/ani/standard/PKMN.gif"]=sprites.dexani.url
    data[item.pokemon]['sprites']["swsh/ani/shiny/PKMN.gif"]=sprites.dexanishiny.url
    data[item.pokemon]['sprites']["swsh/png/standard/PKMN.png"]=sprites.dex.url
    data[item.pokemon]['sprites']["swsh/png/shiny/PKMN.png"]=sprites.dexshiny.url
    data[item.pokemon]['sprites']["bw/png/standard/PKMN.png"]=sprites.bw.url
    data[item.pokemon]['sprites']["bw/png/shiny/PKMN.png"]=sprites.bwshiny.url
    data[item.pokemon]['sprites']["afd/png/standard/PKMN.png"]=sprites.afd.url
    data[item.pokemon]['sprites']["afd/png/shiny/PKMN.png"]=sprites.afdshiny.url
    data=json.dumps(data)
    print(item.pokemon)
    item.data=data
    item.save()


#merge user
accounttodelete=User.objects.get(username="Its_Bruno")
accounttokeep=User.objects.get(username="Bruno")
#historical_teams
for item in historical_team.objects.filter(coach1=accounttodelete):
    item.coach1=accounttokeep
    item.save()
for item in historical_team.objects.filter(coach2=accounttodelete):
    item.coach2=accounttokeep
    item.save()
#coachawards
for item in coachaward.objects.filter(coach=accounttodelete):
    try:
        item.coach=accounttokeep
        item.save()
    except:
        item.delete()
#showdown alts


##fix database
for item in replaydatabase.objects.all():
    try:
        sa=showdownalts.objects.get(showdownalt=item.winneruser)
        if (sa.user != item.winnercoach1) and (sa.user != item.winnercoach2):
            #check if on team 1
            if (sa.user==item.team1coach1) or (sa.user==item.team1coach2):
                #try accessing hist match
                try:
                    hm=item.associatedhistoricmatch
                    hm.winner=hm.team1
                    hm.team1score=hm.team2score
                    hm.team2score=0
                    hm.save()
                    print(f'{item.winneruser} {hm.team1.coach1} {hm.winner.coach1}')
                except:
                    #try accessing hist match
                    try:
                        m=item.associatedmatch
                        m.winner=m.team1
                        m.team1score=m.team2score
                        m.team2score=0
                        m.save()
                        print(f'{item.winneruser} {m.team1.coach} {m.winner.coach}')
                    except:
                        pass
            elif (sa.user==item.team2coach1) or (sa.user==item.team2coach2):
                try:
                    hm=item.associatedhistoricmatch
                    hm.winner=hm.team2
                    hm.team2score=hm.team1score
                    hm.team1score=0
                    hm.save()
                    print(f'{item.winneruser} {hm.team2.coach1} {hm.winner.coach1}')
                except:
                    #try accessing hist match
                    try:
                        m=item.associatedmatch
                        m.winner=m.team2
                        m.team2score=m.team1score
                        m.team1score=0
                        m.save()
                        print(f'{item.winneruser} {m.team2.coach} {m.winner.coach}')
                    except:
                        pass
    except:
        pass

#import trades
with open('trades.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            id_=historical_trading.objects.all().order_by('-id').first().id+1
            sn=row[0]
            tn=row[1]
            pokemon1=row[2]
            pokemon1=get_pkmn(pokemon1)
            pokemon2=row[3]
            pokemon2=get_pkmn(pokemon2)
            print(f'{sn} {tn}')
            toi=historical_team.objects.filter(league__name="SKL",seasonname=sn).get(teamname=tn)
            historical_trading.objects.create(id=id_,team=toi,droppedpokemon=pokemon1,addedpokemon=pokemon2)
            line_count += 1

with open('matchs.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            id_=historical_match.objects.all().order_by('-id').first().id+1
            sn=row[0]
            week=row[1]
            team1=row[2].rstrip()
            team2=row[3].rstrip()
            winner=row[4].rstrip()
            team1score=row[5]
            team2score=row[6]
            replay=row[7]
            team1=historical_team.objects.filter(league__name="SKL",seasonname=sn).get(teamname=team1)
            team2=historical_team.objects.filter(league__name="SKL",seasonname=sn).get(teamname=team2)
            if winner!="":
                winner=historical_team.objects.filter(league__name="SKL",seasonname=sn).get(teamname=winner)
            else:
                winner=None
            historical_match.objects.create(id=id_,week=week,team1=team1,team2=team2,winner=winner,team1score=team1score,team2score=team2score,replay=replay)
            line_count += 1
            print(line_count)