from .killchecks import *
from .luckcheck import *

def gothroughturns(logfile,results):
    turns=results['turns']
    for i in range(len(turns)):
        turndata=turns[i][str(i)]
        #check luck
        results=luckcheck(results,turndata,i)
        results=supportcheck(results,turndata,i)
        results=damagecheck(results,turndata,i)
        for line in turndata:
            #add to line data
            for mon in results['team1']['roster']:
                if line.find(f"p1a: {mon['nickname']}")>-1:
                    mon['lines'].append([i,line])
            for mon in results['team2']['roster']:
                if line.find(f"p2a: {mon['nickname']}")>-1:
                    mon['lines'].append([i,line])
    #go through mons
    #find cause of deaths
    for mon in results['team1']['roster']:
        index=0
        lines_=[]
        causeofdeathlines=[]
        for line in mon['lines']:
            if line[1].split(" ",1)[1].split("|")[0].find(mon['nickname'])>-1:
                causeofdeathlines.append(line)
        for line in causeofdeathlines:
            results=checkdeath(line[1],results,index,causeofdeathlines)
            index+=1
    for mon in results['team2']['roster']:
        index=0
        lines_=[]
        causeofdeathlines=[]
        for line in mon['lines']:
            if line[1].split(" ",1)[1].split("|")[0].find(mon['nickname'])>-1:
                causeofdeathlines.append(line)
        for line in causeofdeathlines:
            results=checkdeath(line[1],results,index,causeofdeathlines)
            index+=1
    results=forfeitadjustment(results,i)
    #investigate deaths
    for mon in results['team1']['roster']:
        if mon['deaths']==0:
            results['team1']['score']+=1
            remaining=100
            for line in mon['lines']:
                if line[1].find("/100")>-1 and line[1].find(f"{mon['nickname']}|")>-1:
                    remaining=int(line[1].split(f"/")[0].split("|")[-1])
            mon['remaininghealth']=remaining    
        else:
            results=killersearch(results,mon,results['team1'],2)
            mon['remaininghealth']=0
        results['team1']['remaininghealth']+=mon['remaininghealth']
        if mon['pokemon']=="Mr. Mime":
            mon['pokemon']="Mr.Mime"
    for mon in results['team2']['roster']:
        if mon['deaths']==0:
            results['team2']['score']+=1
            remaining=100
            for line in mon['lines']:  
                if line[1].find("/100")>-1 and line[1].find(f"{mon['nickname']}|")>-1:
                    remaining=int(line[1].split(f"/")[0].split("|")[-1])
            mon['remaininghealth']=remaining    
        else:
            results=killersearch(results,mon,results['team2'],1)
            mon['remaininghealth']=0
        results['team2']['remaininghealth']+=mon['remaininghealth']
        if mon['pokemon']=="Mr. Mime":
            mon['pokemon']="Mr.Mime"
    results['team1']['remaininghealth']=f"{results['team1']['remaininghealth']}/{100*len(results['team1']['roster'])}"
    results['team2']['remaininghealth']=f"{results['team2']['remaininghealth']}/{100*len(results['team2']['roster'])}"
    return logfile,results

def killersearch(results,mon,roster,otherteam):
    if mon['causeofdeath']=="Direct Damage":
        results=directdamagesearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Burn":
        results=burnsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Poison":
        results=poisonsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Rocky Helmet":
        results=rockyhelmetsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Perish Song":
        results=perishsongsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Black Sludge":
        results=blacksludgesearch(results,mon,roster,otherteam)
    elif mon['causeofdeath'] in ["Explosion","Self-Destruct","Memento","Lunar Dance"] :
        if otherteam==1:
            results['team2']['selfdeaths']+=1
        elif otherteam==2:
            results['team1']['selfdeaths']+=1
        deathturn=mon['lines'][-1][0]
        results['significantevents'].append([deathturn,f'{mon["pokemon"]} killed themself with {mon["causeofdeath"]}'])
    return results

def supportcheck(results,turndata,turn):
    supportmoves=['Reflect','Light Screen','Heal Bell','Aromatherapy','Wish','Stealth Rocks','Spikes','Toxic Spikes','Sticky Web', 'Aurora Veil','Defog','Rapid Spin','Hail','Sandstorm','Sunny Day','Rain Dance','Encore','Taunt','Haze','Clear Smog','Roar','Whirlwind','Leech Seed','Toxic','Will-O-Wisp','Stun Spore','Poison Powder','Block','Mean Look','Dark Void','Destiny Bond','Disable','Electric Terrain','Embargo','Endure','Fairy Lock',"Forest's Curse",'Glare','Grass Whistle','Grassy Terrain','Gravity','Grudge','Heal Block','Healing Wish','Hypnosis','Lucky Chant','Lunar Dance','Magic Coat','Magic Room','Mean Look','Memento','Mist','Misty Terrain','Mud Sport','Parting Shot','Perish Song','Poison Gas','Psychic Terrain','Safeguard','Simple Beam','Sing','Skill Swap','Sleep Powder','Soak','Speed Swap','Spider Web','Spite','Spore','Sweet Kiss','Switcheroo','Tailwind','Thunder Wave','Torment','Toxic Thread','Trick','Trick Room','Water Sport','Wonder Room','Worry Seed','Yawn']
    for line in turndata:
        for move in supportmoves:
            if line.find("|move|p1a: ")>-1 and line.find(f"|{move}|")>-1:
                supportiterator(results,line,'team1',move,turn)
            if line.find("|move|p2a: ")>-1 and line.find(f"|{move}|")>-1:
                supportiterator(results,line,'team2',move,turn)
    return results

def supportiterator(results,line,team,move,turn):
    results[team]['support']+=1
    pokemon=line.split(' ',1)[1].split(f"|{move}")[0]
    for mon in results[team]['roster']:
        if mon['nickname']==pokemon:
            mon['support']+=1
            pokemon=mon['pokemon']
    results['significantevents'].append([turn,f'{pokemon} provided support by using {move}'])
    return results,pokemon

def damagecheck(results,turndata,turn):
    #Stealth Rock, 
    for line in turndata:
        if line.find("|-damage|p1a: ")>-1:
            endhp=line.split("|")[3].split("/")[0].split(" ")[0]
            damagedpokemon=line.split(" ",1)[1].split("|")[0]
            #print(damagedpokemon)
        if line.find("|-damage|p2a: ")>-1:
            endhp=line.split("|")[3].split("/")[0].split(" ")[0]
            damagedpokemon=line.split(" ",1)[1].split("|")[0]
            #print(damagedpokemon)
    return results

def damageiterator(results,line,team,move,turn):
    results[team]['support']+=1
    pokemon=line.split(' ',1)[1].split(f"|{move}")[0]
    for mon in results[team]['roster']:
        if mon['nickname']==pokemon:
            mon['support']+=1
            pokemon=mon['pokemon']
    print(results['significantevents'])
    #results['significantevents'].append([turn,f'{pokemon} provided support by using {move}'])
    return results,pokemon

def checkdeath(line,results,index,turndata):
    if line.find('|faint|p1a')>-1:
        fainted=line.split(" ",1)[1]
        #find cause of death
        causeofdeathline=turndata[index-1][1]
        #print(line)
        #print(causeofdeathline)
        causeofdeath=findcauseofdeath(causeofdeathline)
        for item in results[f'team1']['roster']:
            if item['nickname']==fainted:
                item['deaths']=1
                item['causeofdeath']=causeofdeath
                results['team1']['deaths']+=1
    elif line.find('|faint|p2a')>-1:
        fainted=line.split(" ",1)[1]
        #find cause of death
        causeofdeathline=turndata[index-1][1]
        #print(line)
        #print(causeofdeathline)
        causeofdeath=findcauseofdeath(causeofdeathline)
        for item in results[f'team2']['roster']:
            if item['nickname']==fainted:
                item['deaths']=1
                item['causeofdeath']=causeofdeath
                results['team2']['deaths']+=1
    return results

def findcauseofdeath(causeofdeathline):
    causeofdeath='ded'
    if causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('|[from] item: Rocky Helmet|')>-1:
        causeofdeath="Rocky Helmet"
    elif causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('|[from] psn')>-1:
        causeofdeath="Poison"
    elif causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('|[from] brn')>-1:
        causeofdeath="Burn"
    elif causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('Whirlpool')>-1:
        causeofdeath="Whirlpool"
    elif causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('Infestation')>-1:
        causeofdeath="Infestation"
    elif causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('Iron Barbs')>-1:
        causeofdeath="Iron Barbs"
    elif causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('Rough Skin')>-1:
        causeofdeath="Rough Skin"
    elif causeofdeathline.find('|-damage|')>-1 and causeofdeathline.find('Black Sludge')>-1:
        causeofdeath="Black Sludge"
    elif causeofdeathline.find('perish0')>-1:
        causeofdeath="Perish Song"
    elif causeofdeathline.find('Explosion')>-1:
        causeofdeath="Explosion"
    elif causeofdeathline.find('Lunar Dance')>-1:
        causeofdeath="Lunar Dance"
    elif causeofdeathline.find('|-damage|')>-1:
        causeofdeath="Direct Damage"
    return causeofdeath

def forfeitadjustment(results,i):
    lastturn=results['turns'][i-1][str(i-1)]
    for row in lastturn:
        if row.find('p1a: ')>-1:
            team1lastmon=row.split("p1a: ")[1].split("|")[0]
        if row.find('p2a: ')>-1:
            team2lastmon=row.split("p2a: ")[1].split("|")[0]
    if results['team1']['forfeit']==1:
        for item_ in results[f'team2']['roster']:
            if item_['nickname']==team2lastmon:
                killrecipient=item_
        killstoadd=0
        for item in results[f'team1']['roster']:
            if item['deaths']!=1:
                item['deaths']=1
                item['causeofdeath']="Forfeit"
                results['team1']['deaths']+=1
                results['team2']['kills']+=1
                killstoadd+=1
                results['significantevents'].append([results['numberofturns'],f'{item["pokemon"]} was killed by {killrecipient["pokemon"]} via forfeit.'])
        killrecipient['kills']+=killstoadd
    elif results['team2']['forfeit']==1:
        for item_ in results[f'team1']['roster']:
            if item_['nickname']==team1lastmon:
                killrecipient=item_
        killstoadd=0
        for item in results[f'team2']['roster']:
            if item['deaths']!=1:
                item['deaths']=1
                item['causeofdeath']="Forfeit"
                results['team2']['deaths']+=1
                results['team1']['kills']+=1
                killstoadd+=1
                results['significantevents'].append([results['numberofturns'],f'{item["pokemon"]} was killed by {killrecipient["pokemon"]} via forfeit.'])
        killrecipient['kills']+=killstoadd
    return results

if __name__ == "__main__":
    main()