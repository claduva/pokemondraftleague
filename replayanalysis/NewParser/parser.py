import requests
import json

from .luckfunctions import *

def replay_parse_switch(argument,parsedlogfile,results):
    switcher = {
        'activate': activate_function,
        'cant': cant_function,
        'crit': crit_function,
        'curestatus': curestatus_function,
        'damage': damage_function,
        'detailschange': detailschange_function,
        'drag': switch_drag_function,
        'heal':heal_function,
        'message': message_function,
        'move': move_function,
        'player': player_function,
        'poke': poke_function,
        'replace': replace_function,
        'sethp':sethp_function,
        'start': start_function,
        'status': status_function,
        'switch': switch_drag_function,
        'weather': weather_function,
        'win': win_function,
        'zpower': zpower_function,
        #gen,turn,start,tie,detailschange,transform,formechange,switchout,faint,swap,move,cant,message,start,end,ability,endability,item,enditem,status,curestatus,cureteam,singleturn,singlemove,sidestart,sideend,weather,fieldstart,fieldend,sethp,message,hint,activate,heal,boost,unboost,setboost,swapboost,copyboost,clearboost,clearpositiveboost,clearnegativeboost,invertboost,clearallboost,crit,supereffective,resisted,block,fail,immune,miss,center,notarget,mega,primal,zpower,burst,zbroken,hitcount,waiting,anim
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument[2], lambda argument,parsedlogfile,results: (argument,parsedlogfile,results))
    # Execute the function
    return func(argument,parsedlogfile,results)

def newreplayparse(replay):
    #initialize variables
    if replay.find("logfiles")>-1 and replay.find(".txt")>-1:
        logfile = requests.get(replay).text.splitlines()
    else:
        logfile = requests.get(replay+".log").text.splitlines()   
    parsedlogfile=[]
    line_number=0
    turn_number=0
    #initialize output json
    results=initializeoutput()
    results['replay']=replay
    #iterate through logfile
    for line in logfile:
        if line.find("|")>-1:
            #remove unneeded lines
            line=line.replace(", M","").replace(", F","").replace("-*","").replace(", shiny","").replace(", L50","").replace("-Super","").replace("-Large","").replace("-Small","").replace("-Blue","").replace("-Orange","").replace("Florges-White","Florges").replace("-Pokeball","").replace("-Elegant","").replace("-Indigo","").replace("-Yellow","").replace("-Bug","").replace("-Dark","").replace("-Dragon","").replace("-Electric","").replace("-Fairy","").replace("-Fighting","").replace("-Fire","").replace("-Flying","").replace("-Ghost","").replace("-Grass","").replace("-Ground","").replace("-Ice","").replace("-Normal","").replace("-Poison","").replace("-Psychic","").replace("-Rock","").replace("-Steel","").replace("-Water","").replace("-Douse","").replace("-Burn","").replace("-Chill","").replace("-Shock","").replace("Type: ","Type:").replace("Mr. ","Mr.").replace("-Sensu","").replace("-Pom-Pom","").replace("-Pa'u","").replace("Farfetch'd","Farfetchd").replace("-Totem","").replace("-Resolute","").replace("-Meteor","").replace("Meowstic-F","Meowstic").replace("-East","").replace("Sirfetch'd","Sirfetchd")
            linestoremove=["|","|teampreview","|clearpoke","|upkeep"]
            badlines=["","|start","|player|p1","|player|p2","|player|p1|","|player|p2|","|-notarget","|-clearallboost","|-nothing"]
            linepurposestoremove=["j","c","l","html","raw","teamsize","gen","gametype","tier","rule","-mega","seed","teampreview","anim"]
            linepurpose=line.split("|",2)[1].replace("-","")
            #iterate turn number
            if linepurpose=="turn":
                turn_number+=1
                results['numberofturns']=turn_number
            #add turn data
            elif line not in linestoremove and linepurpose not in linepurposestoremove and line not in badlines:
                lineremainder=line.split("|",2)[2]
                if lineremainder.find("/")>-1:
                    lineremainder_=""
                    for segment in lineremainder.split("|"):
                        if segment.find("/")>-1:
                            try:
                                numerator=segment.split("/")[0]
                                denomenator=segment.split("/")[1].split("|")[0].split(" ")[0]
                                newnumerator=int(int(numerator)/int(denomenator)*100)
                                if newnumerator==0: newnumerator=1
                                segment=segment.replace(f"/{denomenator}","/100").replace(f"{numerator}/",f"{newnumerator}/")
                            except:
                                pass
                        lineremainder_=lineremainder_+"|"+segment    
                    lineremainder=lineremainder_[1:]
                parsedlogfile.append([line_number,turn_number,linepurpose,lineremainder])
                line_number+=1
    #iterate through parsed logfile
    for line in parsedlogfile:
        line,parsedlogfile,results=replay_parse_switch(line,parsedlogfile,results)
    #sort significant events
    results['significantevents']=sorted( results['significantevents'],key=lambda tup: tup[0])
    #update result totals
    teams=['team1','team2']
    categories=['kills','deaths','luck','support','hphealed','damagedone','remaininghealth']
    for team in teams:
        for mon in results[team]['roster']:
            results[team]['score']+=1-mon['deaths']
            for category in categories:
                results[team][category]+=mon[category]
                results[team][category]=round(results[team][category],2)
            mon['luck']= mon['luck']/100
            results[team]['totalhealth']+=100
        results[team]['luck']=results[team]['luck']/100
    #output results to json file
    with open('replayanalysis/NewParser/results.json', 'w') as f:
        json.dump(results,f,indent=2)
    #team1
    damagedone=results['team1']['damagedone']
    damagedonetest=results['team2']['totalhealth']-results['team2']['remaininghealth']+results['team2']['hphealed']
    score=results['team1']['score']
    scoretest=len(results['team1']['roster'])-results['team2']['kills']-results['team1']['selfdeaths']
    if damagedonetest!=damagedone: results['errormessage'].append("This replay's Team 1 damage numbers do not add up. Please contact claduva and do not submit the replay.")
    if scoretest!=score: results['errormessage'].append("This replay's Team 1 score numbers do not add up. Please contact claduva and do not submit the replay.")
    if score!=0 and results['team2']['wins']==1: results['errormessage'].append("The losing team's score should be 0. Please contact claduva and do not submit the replay.")
    #team2
    damagedone=results['team2']['damagedone']
    damagedonetest=results['team1']['totalhealth']-results['team1']['remaininghealth']+results['team1']['hphealed']
    score=results['team2']['score']
    scoretest=len(results['team2']['roster'])-results['team1']['kills']-results['team2']['selfdeaths']
    if damagedonetest!=damagedone: results['errormessage'].append("This replay's Team 2 damage numbers do not add up. Please contact claduva and do not submit the replay.")
    if scoretest!=score: results['errormessage'].append("This replay's Team 2 score numbers do not add up. Please contact claduva and do not submit the replay.")
    if score!=0 and results['team1']['wins']==1: results['errormessage'].append("The losing team's score should be 0. Please contact claduva and do not submit the replay.")
    if len(results['errormessage'])>0:
        results=alternativereplayparse(replay)
    return results

def activate_function(line,parsedlogfile,results):
    if line[3].split("|")[1]=="confusion":
        defendingteam=line[3].split(":",1)[0]
        if defendingteam=="p1a":
            defender=roster_search(defendingteam,results['team1']['activemon'],results)
            attacker=roster_search("p2a",results['team2']['activemon'],results)
        elif defendingteam=="p2a":
            defender=roster_search(defendingteam,results['team2']['activemon'],results)
            attacker=roster_search("p1a",results['team1']['activemon'],results)
        attacker['luck']+=-33
        defender['luck']+=33
    elif line[3].find("|move: Destiny Bond")>-1:
        team=line[3].split(": ")[0]
        killer=line[3].split("|")[0].split(": ")[1]
        killer=roster_search(team,killer,results)
        fainted=list(filter(lambda x: x[0] > line[0] and x[1] == line[1] and x[2]=="faint", parsedlogfile))[0]
        faintedteam=fainted[3].split(": ")[0]
        faintedmon=fainted[3].split(": ")[1]
        fainted=roster_search(faintedteam,faintedmon,results)
        killer['damagedone']+=fainted['remaininghealth']; killer['kills']+=1
        fainted['remaininghealth']=0; fainted['deaths']=1
    return line,parsedlogfile,results

def cant_function(line,parsedlogfile,results):
    reason=line[3].split("|")[1]
    team=line[3].split(":")[0]
    pokemon=line[3].split("|")[0].split(": ")[1]
    pokemon=roster_search(team,pokemon,results)
    if team=="p1a":
        activemon=results['team2']['activemon']
        activemon=roster_search('p2a',activemon,results)
    elif team=="p2a":
        activemon=results['team1']['activemon']
        activemon=roster_search('p1a',activemon,results)
    if reason=="frz":
        pokemon['luck']+=-20
        activemon['luck']+=20
    elif reason=="par":
        pokemon['luck']+=-75
        activemon['luck']+=75
    return line,parsedlogfile,results

def curestatus_function(line,parsedlogfile,results):
    team=line[3].split(":",1)[0]
    mon=line[3].split("|",1)[0].split(" ",1)[1]
    status=line[3].split("|")[1]
    mon=roster_search(team,mon,results)
    mon[status]=None
    return line,parsedlogfile,results

def damage_function(line,parsedlogfile,results):
    team=line[3].split(":",1)[0]
    if team=="p1a":
        otherteam="p2a";otherteam_="team2";thisteam="team1"
    elif team=="p2a":
        otherteam="p1a";otherteam_="team1";thisteam="team2"
    pokemon=line[3].split(" ",1)[1].split("|")[0]
    healthremaining=int(line[3].split("|",1)[1].split(" ",1)[0].split("/",1)[0].split("|",1)[0])
    #searchroster
    pokemon=roster_search(team,pokemon,results)
    #update remaining health
    previoushealth=pokemon['remaininghealth']
    pokemon['remaininghealth']=healthremaining
    damagedone=previoushealth-healthremaining
    #determine damager
    if line[3].find("[from]")>-1:
        #not direct damage
        cause=line[3].split("[from] ")[1]
        if cause=="stealthrock": cause='Stealth Rock'
        damager=None ;move=None
        if cause=="psn" and pokemon[cause]==None:
            cause="tox"
        if cause in ['Stealth Rock','Spikes']:
            damager=roster_search(otherteam,results[thisteam][cause],results)
        elif cause.title() in ['Sandstorm','Hail']:
            if results[thisteam][cause.title()]!=None:
                damager=roster_search(otherteam,results[thisteam][cause.title()],results)
            elif results[otherteam_][cause.title()]!=None:
                setter=roster_search(team,results[otherteam_][cause.title()],results)
                setter['hphealed']+=-damagedone
        elif cause.find("item: Rocky Helmet")>-1 or cause.find("Leech Seed")>-1 or cause.find("ability: Iron Barbs")>-1 or cause.find("ability: Rough Skin")>-1 or cause.find("ability: Aftermath")>-1 or cause.find("ability: Liquid Ooze")>-1 or cause.find("ability: Innards Out")>-1 or cause.find("ability: Bad Dreams")>-1  or cause.find("Spiky Shield")>-1 or cause.find("leechseed")>-1:
            damager=cause.split("|[of] ")[1].split(": ",1)[1]
            team=cause.split("|[of] ")[1].split(": ",1)[0]
            damager=roster_search(team,damager,results)
        elif cause.find("move: Whirlpool")>-1 or cause.find("move: Infestation")>-1 or cause.find("move: Magma Storm")>-1 or cause.find("move: Wrap")>-1 or cause.find("move: Fire Spin")>-1 or cause.find("move: Sand Tomb")>-1 or cause.find("ability: Disguise|[of]")>-1 or cause.find("mimikyubusted")>-1:
            if team=="p1a":
                damager=results['team2']['activemon']
                damager=roster_search("p2a",damager,results)
            elif team=="p2a":
                damager=results['team1']['activemon']
                damager=roster_search("p1a",damager,results)
        elif cause.find("ability: Solar Power")>-1 or cause.find("ability: Dry Skin")>-1:
            pokemon['hphealed']+=-damagedone
        elif cause in ['Recoil','item: Life Orb','highjumpkick','recoil','High Jump Kick','Mind Blown','steelbeam','mindblown','Steel Beam'] or cause.find("Recoil|[of] ")>-1 or cause.find("recoil|[of] ")>-1:
            pokemon['hphealed']+=-damagedone
        elif cause in ["item: Black Sludge","item: Sticky Barb"]:
            matchdata=list(filter(lambda x: x[0] < line[0], parsedlogfile))[::-1]
            switched=False
            accounted=False
            for line_ in matchdata:
                if line_[2]=="item" and line_[3].find(cause.split(": ",1)[1])>-1 and line_[3].find(pokemon['nickname'])>-1:
                    switched=True
                if line_[2]=="move" and line_[3].split("|")[1] in ['Trick','Switcheroo'] and switched==True and line_[3].split("|")[0].split(": ",1)[1]!=pokemon['nickname']:
                    damager=line_[3].split("|")[0].split(": ",1)[1]
                    team=line_[3].split(": ",1)[0]
                    damager=roster_search(team,damager,results)
                    accounted=True
                    break
                elif line_[2]=="move" and line_[3].split("|")[1] in ['Trick','Switcheroo'] and switched==False and line_[3].split("|")[0].split(": ",1)[1]==pokemon['nickname']:
                    pokemon['hphealed']+=-damagedone
                    accounted=True
                    break
            if accounted==False:
                pokemon['hphealed']+=-damagedone
        else:
            if pokemon[cause]==pokemon['nickname']:
                pokemon['hphealed']+=-damagedone
            else:
                if cause in ['psn','tox'] and pokemon[cause]==None:
                    pokemon[cause]=results[thisteam]['Toxic Spikes']
                if pokemon[cause]==None and pokemon['pokemon'] in ['Zoroark','Zorua']: 
                    for mon in results[thisteam]['roster']:
                        if mon[cause]!=None:
                            pokemon[cause]=mon[cause]
                            break
                damager=roster_search(otherteam,pokemon[cause],results)
        if damager:
            damager['damagedone']+=damagedone 
        if cause=="confusion":
            activeopponent=roster_search(otherteam,results[otherteam_]['activemon'],results)
            results['significantevents'].append([line[1],f"LUCK: {pokemon['pokemon']} hit itself in confusion caused by {pokemon['confusion']}."])
            pokemon['luck']+=-100
            activeopponent['luck']+=100
    else:
        #search for damager
        damager,move=damager_search(parsedlogfile,line,team,pokemon,results,damagedone)
    #update fainted
    if healthremaining==0:
        pokemon['deaths']=1
        if damager and move: 
            damager['kills']+=1
            results['significantevents'].append([line[1],f"{damager['pokemon']} killed {pokemon['pokemon']} with {move}"])
        elif damager and cause: 
            damager['kills']+=1
            results['significantevents'].append([line[1],f"{damager['pokemon']} killed {pokemon['pokemon']} via {cause}"])
        else:
            results['significantevents'].append([line[1],f"{pokemon['pokemon']} fainted via {cause}"])
            results[thisteam]['selfdeaths']+=1
    return line,parsedlogfile,results

def damager_search(parsedlogfile,line,team,pokemon,results,damagedone):
    damager=None
    move=None
    turndata=list(filter(lambda x: x[1] == line[1] and x[0] < line[0], parsedlogfile))[::-1]
    for line in turndata:
        if team=="p1a":
            if line[2]=="end" and line[3].find(f"p1a: {pokemon['nickname']}")>-1 and line[3].find("|move: Future Sight")>-1:
                damager=roster_search("p2a",results['team1']['Future Sight'],results)
                damager['damagedone']+=damagedone
                move="Future Sight"
                break
            elif line[2]=="end" and line[3].find(f"p1a: {pokemon['nickname']}")>-1 and line[3].find("|move: Doom Desire")>-1:
                damager=roster_search("p2a",results['team1']['Doom Desire'],results)
                damager['damagedone']+=damagedone
                move="Doom Desire"
                break
            elif line[2]=="start" and line[3].find(f"p1a: {pokemon['nickname']}")>-1 and line[3].find("|Substitute")>-1:
                pokemon['hphealed']+=-damagedone
                break
            elif line[2] in ["move","prepare"] and line[3].split(":",1)[0]=="p2a" and line[3].find(f"p1a: {pokemon['nickname']}")>-1:
                damager=line[3].split(" ",1)[1].split("|",1)[0]
                damager=roster_search("p2a",damager,results)
                damager['damagedone']+=damagedone
                move=line[3].split("|")[1]
                break
            elif line[2] in ["move","prepare"] and line[3].split(":",1)[0]=="p2a" and line[3].find("[still]")>-1:
                damager=line[3].split(" ",1)[1].split("|",1)[0]
                damager=roster_search("p2a",damager,results)
                damager['damagedone']+=damagedone
                move=line[3].split("|")[1]
                break
        elif team=="p2a":
            if line[2]=="end" and line[3].find(f"p2a: {pokemon['nickname']}")>-1 and line[3].find("|move: Future Sight")>-1:
                damager=roster_search("p1a",results['team2']['Future Sight'],results)
                damager['damagedone']+=damagedone
                move="Future Sight"
                break
            elif line[2]=="end" and line[3].find(f"p2a: {pokemon['nickname']}")>-1 and line[3].find("|move: Doom Desire")>-1:
                damager=roster_search("p1a",results['team2']['Doom Desire'],results)
                damager['damagedone']+=damagedone
                move="Doom Desire"
                break
            elif line[2]=="start" and line[3].find(f"p2a: {pokemon['nickname']}")>-1 and line[3].find("|Substitute")>-1:
                pokemon['hphealed']+=-damagedone
                break
            elif line[2] in ["move","prepare"] and line[3].split(":",1)[0]=="p1a" and line[3].find(f"p2a: {pokemon['nickname']}")>-1:
                damager=line[3].split(" ",1)[1].split("|",1)[0]
                damager=roster_search("p1a",damager,results)
                damager['damagedone']+=damagedone
                move=line[3].split("|")[1]
                break
            elif line[2] in ["move","prepare"] and line[3].split(":",1)[0]=="p1a" and line[3].find("[still]")>-1:
                damager=line[3].split(" ",1)[1].split("|",1)[0]
                damager=roster_search("p1a",damager,results)
                damager['damagedone']+=damagedone
                move=line[3].split("|")[1]
                break
    return damager,move

def detailschange_function(line,parsedlogfile,results):
    if line[3].split(":",1)[0]=="p1a" and line[3].find("-Mega")>-1:
        results,line=replacemega(results,line,1)
    elif line[3].split(":",1)[0]=="p2a" and line[3].find("-Mega")>-1:
        results,line=replacemega(results,line,2)  
    return line,parsedlogfile,results

def heal_function(line,parsedlogfile,results):
    team=line[3].split(":",1)[0]
    pokemon=line[3].split(" ",1)[1].split("|")[0]
    healthremaining=int(line[3].split("|",1)[1].split("/",1)[0])
    #searchroster
    pokemon=roster_search(team,pokemon,results)
    #update remaining health
    previoushealth=pokemon['remaininghealth']
    pokemon['remaininghealth']=healthremaining
    healthhealed=healthremaining-previoushealth
    #update health healed
    if line[3].find("|[wisher] ")==-1 and line[3].find("[from] move: Lunar Dance")==-1:   
        pokemon['hphealed']+=healthhealed
    elif line[3].find("[from] move: Lunar Dance")>-1 or line[3].find("[from] move: Healing Wish")>-1:   
        turndata=list(filter(lambda x: x[1] == line[1] and x[0] < line[0], parsedlogfile))[::-1]
        for line_ in turndata:
            if line_[2]=="move" and line_[3].split("|")[1] in ['Healing Wish','Lunar Dance']:
                healer=line_[3].split("|")[0].split(": ",1)[1]
                healer=roster_search(team,healer,results)
                healer['hphealed']+=healthhealed
    else:
        wisher=line[3].split("|[wisher] ")[1]
        wisher=roster_search(team,wisher,results)
        wisher['hphealed']+=healthhealed
    return line,parsedlogfile,results

def message_function(line,parsedlogfile,results):
    line[3]=line[3].replace("lost due to inactivity.","forfeited.")
    if line[3].find("forfeited.")>-1:
        ffcoach=line[3].split(" forfeited.")[0]
        if ffcoach == results['team1']['coach']:
            results['team1']['forfeit']=1
            lastactivemon=results['team2']['activemon']
            lastactivemon=roster_search('p2a',lastactivemon,results)
            for mon in results['team1']['roster']:
                if mon['deaths']==0:
                    lastactivemon['kills']+=1
                mon['deaths']=1
        elif ffcoach == results['team2']['coach']:
            results['team2']['forfeit']=1
            lastactivemon=results['team1']['activemon']
            lastactivemon=roster_search('p1a',lastactivemon,results)
            for mon in results['team2']['roster']:
                if mon['deaths']==0:
                    lastactivemon['damagedone']+=mon['remaininghealth']
                    mon['remaininghealth']=0
                    lastactivemon['kills']+=1
                    mon['deaths']=1
    return line,parsedlogfile,results

def move_function(line,parsedlogfile,results):
    #parse line
    move=line[3].split("|")[1]
    attackingteam=line[3].split(":",1)[0]
    attacker=line[3].split("|",1)[0].split(" ",1)[1]
    attacker=roster_search(attackingteam,attacker,results)
    try:
        defendingteam=line[3].split("|")[2].split(":",1)[0]
        target=line[3].split("|")[2].split(" ",1)[1]
        target=roster_search(defendingteam,target,results)
    except:
        defendingteam=None; target=None
    #check for 2 turn moves
    if line[3].find("[still]")>-1:
        return line,parsedlogfile,results
    #support moves
    supportmoves=['Reflect','Light Screen','Heal Bell','Aromatherapy','Wish','Stealth Rock','Spikes','Toxic Spikes','Sticky Web', 'Aurora Veil','Defog','Rapid Spin','Hail','Sandstorm','Sunny Day','Rain Dance','Encore','Taunt','Haze','Clear Smog','Roar','Whirlwind','Leech Seed','Toxic','Will-O-Wisp','Stun Spore','Poison Powder','Block','Mean Look','Dark Void','Destiny Bond','Disable','Electric Terrain','Embargo','Endure','Fairy Lock',"Forest's Curse",'Glare','Grass Whistle','Grassy Terrain','Gravity','Grudge','Heal Block','Healing Wish','Hypnosis','Lucky Chant','Lunar Dance','Magic Coat','Magic Room','Mean Look','Memento','Mist','Misty Terrain','Mud Sport','Parting Shot','Perish Song','Poison Gas','Psychic Terrain','Safeguard','Simple Beam','Sing','Skill Swap','Sleep Powder','Soak','Speed Swap','Spider Web','Spite','Spore','Sweet Kiss','Switcheroo','Tailwind','Thunder Wave','Torment','Toxic Thread','Trick','Trick Room','Water Sport','Wonder Room','Worry Seed','Yawn']
    #check for support
    if move in supportmoves:
        attacker['support']+=1
        results['significantevents'].append([line[1],f"{attacker['pokemon']} provided support by using {move}"])
    #check for hazards
    hazardmoves=["Stealth Rock","Spikes","Toxic Spikes"]
    if move in hazardmoves:
        if attackingteam=="p1a":
            results['team2'][move]=attacker['nickname']
        elif attackingteam=="p2a":
            results['team1'][move]=attacker['nickname']
    #moves that can miss
    movesthatcanmiss=dict([['Precipice Blades', 85], ['High Horsepower', 95], ['Sand Tomb', 85], ['Triple Kick', 90], ['Tail Slap', 85], ['Double Slap', 85], ['Sky Uppercut', 90], ['Super Fang', 90], ['Hyper Beam', 90], ['Dynamic Punch', 50], ['Focus Blast', 70], ['Ice Ball', 90], ['Crush Claw', 95], ['Leech Seed', 90], ['Metal Claw', 95], ['Magma Storm', 75], ['Aeroblast', 95], ['Thunder Wave', 90], ['Head Smash', 80], ['Sing', 55], ['Blizzard', 70], ['Blast Burn', 90], ['Pin Missile', 95], ['Overheat', 90], ['Swagger', 85], ['Flying Press', 95], ['Fly', 95], ['Poison Gas', 90], ['Crabhammer', 90], ['Razor Leaf', 95], ['Poison Powder', 75], ['Rock Tomb', 95], ['Power Whip', 85], ['Supersonic', 55], ['Bind', 85], ['Fissure', 30], ['Sweet Kiss', 75], ['Play Rough', 90], ['Fury Swipes', 80], ['Zen Headbutt', 90], ['Belch', 90], ['Fury Cutter', 95], ['Iron Tail', 75], ['Toxic', 90], ['Egg Bomb', 75], ['Shadow Strike', 95], ['Thunder Fang', 95], ['Charge Beam', 90], ['Lovely Kiss', 75], ['Clamp', 85], ['Rock Throw', 90], ['Ice Fang', 95], ['Electroweb', 95], ['Whirlpool', 85], ['Smog', 70], ['Icy Wind', 95], ['Steel Wing', 90], ['Sonic Boom', 90], ['Hypnosis', 60], ['Fire Fang', 95], ['Seed Flare', 85], ['Hydro Cannon', 90], ['Jump Kick', 95], ['Leaf Storm', 90], ['Bolt Strike', 85], ['Air Cutter', 95], ['Mega Kick', 75], ['Inferno', 50], ['Rock Climb', 85], ['Rock Blast', 90], ['Freeze Shock', 90], ['Drill Run', 95], ['Floaty Fall', 95], ['Fire Spin', 85], ['Frenzy Plant', 90], ['Bone Rush', 90], ['Guillotine', 30], ['Slam', 75], ['Aqua Tail', 90], ['Diamond Storm', 95], ['Metal Sound', 85], ['Psycho Boost', 90], ['Gear Grind', 85], ['Barrage', 85], ['Bonemerang', 90], ['Draco Meteor', 90], ['Leaf Tornado', 90], ['Hyper Fang', 90], ['Muddy Water', 85], ['Thunder', 70], ['Sleep Powder', 75], ['Hammer Arm', 90], ['Origin Pulse', 85], ['Kinesis', 80], ['Grass Whistle', 55], ['Bone Club', 85], ['Fire Blast', 85], ['Mud Bomb', 85], ['Sheer Cold', 30], ['Frost Breath', 90], ['Roar of Time', 90], ['Hydro Pump', 80], ['Fury Attack', 85], ['High Jump Kick', 90], ['Steam Eruption', 95], ['Mega Punch', 85], ['Stun Spore', 75], ['Night Daze', 95], ['Dragon Tail', 90], ['Horn Drill', 30], ['String Shot', 95], ['Ice Hammer', 90], ['V-create', 95], ['Mud Shot', 95], ['Present', 90], ['Mirror Shot', 85], ['Megahorn', 85], ['Screech', 85], ['Sacred Fire', 95], ['Take Down', 85], ['Zap Cannon', 50], ['Octazooka', 85], ['Double Hit', 90], ['Snarl', 95], ['Stone Edge', 80], ['Rock Wrecker', 90], ['Cut', 95], ['Comet Punch', 85], ['Air Slash', 95], ['Fleur Cannon', 90], ['Dragon Rush', 75], ['Submission', 80], ['Circle Throw', 90], ['Bounce', 85], ['Giga Impact', 90], ['Hurricane', 70], ['Ice Burn', 90], ['Cross Chop', 80], ['Gunk Shot', 80], ['Blaze Kick', 90], ['Meteor Mash', 90], ['Dark Void', 50], ['Dual Chop', 90], ['Rollout', 90], ['Wrap', 90], ['Icicle Crash', 90], ['Will-O-Wisp', 85], ['Glaciate', 95], ['Spacial Rend', 95], ['Light of Ruin', 90], ["Nature's Madness", 90], ['Rock Slide', 90], ['Heat Wave', 90], ['Razor Shell', 95], ['Rolling Kick', 85], ['Blue Flare', 85], ['Sky Attack', 90]])
    #check if can miss
    if move in movesthatcanmiss.keys():
        try: 
            attacker['luck']+=100-movesthatcanmiss[move]
            target['luck']+=-(100-movesthatcanmiss[move])
        except:
            pass
    #check for miss
    if line[3].find("|[miss]")>-1:
        results=miss_function(line,attacker,target,move,results)
    #check if can crit
    movesthatcancrit=['Precipice Blades', 'Steel Beam','Thunder Punch', 'Scratch', 'High Horsepower', 'Anchor Shot', 'Avalanche', 'Sand Tomb', 'Fire Punch', 'Infestation', 'Superpower', 'Zing Zap', 'Giga Drain', 'Chatter', 'Black Hole Eclipse', 'Bloom Doom', 'Triple Kick', 'Night Slash', 'Plasma Fists', 'Extrasensory', 'Ice Punch', 'Tail Slap', 'Double Slap', 'Thunder Shock', 'Splintered Stormshards', 'Sky Uppercut', 'Hyper Beam', 'Dynamic Punch', 'Poison Sting', 'Dig', 'Focus Blast', 'Liquidation', 'Double Kick', 'Ice Ball', 'Round', 'False Swipe', 'Crush Claw', 'Shadow Sneak', 'Tectonic Rage', 'Hidden Power Electric', 'Seed Bomb', 'Hidden Power Fire', 'Chip Away', 'Metal Claw', 'Acid', 'Vital Throw', 'Shock Wave', 'Baddy Bad', 'Accelerock', 'Aurora Beam', 'Heart Stamp', 'Magma Storm', 'Crunch', 'Aeroblast', 'Explosion', 'Gigavolt Havoc', 'Moongeist Beam', 'Revenge', 'Clear Smog', 'Wake-Up Slap', 'Pursuit', 'Head Smash', 'Earthquake', 'Incinerate', 'Water Pulse', 'Dragon Pulse', 'Glitzy Glow', 'Acid Spray', 'Blizzard', 'Blast Burn', 'Paleo Wave', 'Mud-Slap', 'Inferno Overdrive', 'Freeze-Dry', 'Pin Missile', 'Overheat', 'Savage Spin-Out', 'First Impression', 'Flame Charge', 'Dizzy Punch', 'Flying Press', 'Lunge', 'Prismatic Laser', 'Fly', 'U-turn', 'Future Sight', 'Fire Lash', 'Smelling Salts', 'Burn Up', 'Catastropika', 'Bug Bite', 'Hidden Power Ghost', 'Relic Song', 'Shell Trap', 'Hyperspace Hole', 'Fake Out', 'Sky Drop', 'Crabhammer', 'Light That Burns the Sky', 'Darkest Lariat', 'Hidden Power', 'Razor Leaf', 'Head Charge', 'Dive', 'Signal Beam', 'Rock Tomb', 'Power Whip', 'Buzzy Buzz', 'Ancient Power', "Let's Snuggle Forever", 'Psychic Fangs', 'Bind', 'Throat Chop', 'Parabolic Charge', 'Retaliate', 'Steamroller', 'Bullet Seed', 'Bubble Beam', 'Freezy Frost', 'Aqua Jet', 'Sludge', 'Bulldoze', 'Flame Burst', 'Thief', 'Play Rough', 'Astonish', 'Dream Eater', 'Energy Ball', 'Fury Swipes', 'Zen Headbutt', 'Belch', 'Power Trip', 'Fury Cutter', 'Iron Tail', 'Clanging Scales', 'Hidden Power Flying', 'Egg Bomb', 'Payback', 'Fusion Flare', 'Boomburst', 'Shadow Strike', 'Secret Sword', 'Thunder Fang', 'Charge Beam', 'Rapid Spin', 'Skull Bash', 'Clamp', 'Hidden Power Dragon', 'Rock Throw', 'Secret Power', 'Fairy Wind', 'Water Shuriken', 'Struggle Bug', 'Corkscrew Crash', 'Ice Fang', 'Self-Destruct', 'Sinister Arrow Raid', 'Stored Power', 'Hidden Power Psychic', 'Tri Attack', 'Psychic', 'Electroweb', 'Weather Ball', 'Shattered Psyche', 'Whirlpool', 'Smog', 'Assurance', 'Icy Wind', 'Steel Wing', 'Core Enforcer', 'Synchronoise', 'Zippy Zap', 'Petal Dance', 'Struggle', 'Iron Head', 'Trop Kick', 'Headbutt', 'Drain Punch', 'Body Slam', 'Bug Buzz', 'Fire Fang', 'Seed Flare', 'Hydro Cannon', 'Mist Ball', 'Jump Kick', 'Water Spout', 'Leaf Storm', 'Ice Shard', 'Earth Power', 'Stomping Tantrum', 'Bolt Strike', 'Bite', 'Air Cutter', 'Sappy Seed', 'Mega Kick', 'Inferno', 'Flamethrower', 'Rock Climb', 'Rock Blast', 'Feint', 'Sucker Punch', 'Doom Desire', 'Dragon Ascent', 'Freeze Shock', 'Peck', 'Drill Run', 'Leafage', 'Sunsteel Strike', 'Dark Pulse', 'Flash Cannon', 'Floaty Fall', 'Poison Fang', 'Twinkle Tackle', 'Dazzling Gleam', 'Double-Edge', 'Hidden Power Rock', 'Sludge Bomb', 'Lick', 'Fire Spin', 'Frenzy Plant', 'Close Combat', 'Bone Rush', 'Slam', 'Aqua Tail', 'Strength', 'Fusion Bolt', 'Rage', 'Diamond Storm', 'Hidden Power Dark', 'Psycho Boost', 'Surf', 'Never-Ending Nightmare', 'Gear Grind', 'Shadow Ball', 'Eruption', 'Barrage', 'Shadow Force', 'Bonemerang', 'Cross Poison', 'Draco Meteor', 'Low Sweep', 'Sludge Wave', 'Leaf Tornado', 'Hyper Fang', 'Covet', 'Hyperspace Fury', 'Karate Chop', 'Fell Stinger', 'Muddy Water', 'Thunder', 'Constrict', 'Razor Wind', 'Water Pledge', 'Brine', 'Hammer Arm', 'Last Resort', 'Pulverizing Pancake', 'Bullet Punch', 'Brick Break', 'Pay Day', 'Oblivion Wing', 'Outrage', 'Origin Pulse', 'Stomp', 'Poison Tail', 'Bone Club', 'Fire Blast', 'Malicious Moonsault', 'Brave Bird', 'Gust', 'Mud Bomb', 'Leaf Blade', 'Sparkly Swirl', 'Twineedle', 'Solar Blade', 'Splishy Splash', 'Spirit Shackle', 'Beak Blast', 'Continental Crush', 'Mystical Fire', 'Confusion', 'Pluck', 'Frost Breath', 'Roar of Time', 'Hydro Pump', 'Fury Attack', 'Swift', 'High Jump Kick', 'Brutal Swing', 'Steam Eruption', 'Petal Blizzard', 'Menacing Moonraze Maelstrom', 'Wing Attack', 'Smart Strike', 'Hidden Power Steel', 'Wood Hammer', 'Hidden Power Water', 'X-Scissor', 'Fiery Dance', 'Echoed Voice', 'Smack Down', "Land's Wrath", 'Disarming Voice', 'Mega Punch', 'Revelation Dance', 'Night Daze', 'Dragon Tail', 'Flare Blitz', 'Ice Hammer', 'Water Gun', 'V-create', 'Acid Downpour', 'Draining Kiss', 'Mud Shot', 'Clangorous Soulblaze', 'Mirror Shot', 'Megahorn', 'Thrash', 'Volt Switch', 'Pound', 'Shadow Claw', 'Sacred Fire', 'Ice Beam', 'Facade', 'Vice Grip', "Magikarp's Revenge", 'Hidden Power Ice', 'Extreme Speed', 'Poison Jab', 'Take Down', 'Phantom Force', 'Double Iron Bash', 'Nuzzle', 'Mind Blown', 'Multi-Attack', 'Zap Cannon', 'Magnet Bomb', 'Absorb', 'Waterfall', 'Hidden Power Fighting', 'Judgment', 'Hidden Power Bug', 'Psybeam', 'Knock Off', 'Octazooka', 'Hyper Voice', 'Double Hit', 'Snarl', 'Spark', 'Stone Edge', 'Venoshock', 'Rock Wrecker', 'Bouncy Bubble', 'Thousand Arrows', 'Needle Arm', 'Dragon Breath', 'Searing Sunraze Smash', 'Cut', 'Comet Punch', 'Aerial Ace', 'Air Slash', 'Leech Life', 'Acrobatics', 'Fleur Cannon', 'Dragon Rush', 'Solar Beam', 'Silver Wind', 'Mach Punch', 'Luster Purge', 'Breakneck Blitz', 'Snore', 'Submission', 'Vacuum Wave', 'Thunderbolt', 'Circle Throw', 'All-Out Pummeling', 'Flame Wheel', 'Hidden Power Poison', 'Subzero Slammer', 'Fire Pledge', 'Bounce', 'Photon Geyser', 'Giga Impact', 'Dragon Claw', 'Soul-Stealing 7-Star Strike', 'Scald', 'Magical Leaf', 'Uproar', 'Force Palm', 'Hurricane', 'Ice Burn', 'Cross Chop', 'Psyshock', 'Hidden Power Grass', '10,000,000 Volt Thunderbolt', 'Techno Blast', 'Gunk Shot', 'Wild Charge', 'Dragon Hammer', 'Horn Attack', 'Blaze Kick', 'Lava Plume', 'Psystrike', 'Spike Cannon', 'Meteor Mash', 'Horn Leech', 'Searing Shot', 'Supersonic Skystrike', 'Arm Thrust', 'Dual Chop', 'Shadow Punch', 'Foul Play', 'Twister', 'Focus Punch', 'Slash', 'Rollout', 'Icicle Spear', 'Feint Attack', 'Wrap', 'Icicle Crash', 'Devastating Drake', 'Pollen Puff', 'Sacred Sword', 'Hex', 'Bubble', 'Quick Attack', 'Glaciate', 'Psycho Cut', 'Sizzly Slide', 'Rock Smash', 'Volt Tackle', 'Oceanic Operetta', 'Grass Pledge', 'Sparkling Aria', 'Attack Order', 'Vine Whip', 'Ember', 'Spacial Rend', 'Light of Ruin', 'Stoked Sparksurfer', 'Powder Snow', 'Hold Back', 'Power-Up Punch', 'Spectral Thief', 'Moonblast', 'Hydro Vortex', 'Thousand Waves', 'Rock Slide', 'Aura Sphere', 'Shadow Bone', 'Drill Peck', 'Storm Throw', 'Heat Wave', 'Tackle', 'Discharge', 'Ominous Wind', 'Razor Shell', 'Hidden Power Ground', 'Rolling Kick', 'Blue Flare', 'Sky Attack', 'Power Gem', 'Mega Drain', 'Genesis Supernova']
    if move in movesthatcancrit:
        try:
            attacker['luck']+=-4
            target['luck']+=4
        except:
            pass
    #moves with secondary effect
    moveswithsecondaryeffect=dict([['Thunder Punch', ['par', 10]],['Thunder Fang', ['par', 10]],['Ice Fang', ['frz', 10]],['Fire Fang', ['brn', 10]], ['Fire Punch', ['brn', 10]], ['Zing Zap', ['flinch', 30]], ['Extrasensory', ['flinch', 10]], ['Ice Punch', ['frz', 10]], ['Thunder Shock', ['par', 10]], ['Poison Sting', ['psn', 30]], ['Focus Blast', ['boosts spd: -1 ', 10]], ['Liquidation', ['boosts def: -1 ', 20]], ['Crush Claw', ['boosts def: -1 ', 50]], ['Metal Claw', ['self boosts: atk: 1 ', 10]], ['Acid', ['boosts spd: -1 ', 10]], ['Aurora Beam', ['boosts atk: -1 ', 10]], ['Heart Stamp', ['flinch', 30]], ['Crunch', ['boosts def: -1 ', 20]], ['Strange Steam', ['confusion', 20]], ['Water Pulse', ['confusion', 20]], ['Blizzard', ['frz', 10]], ['Paleo Wave', ['boosts atk: -1 ', 20]], ['Freeze-Dry', ['frz', 10]], ['Dizzy Punch', ['confusion', 20]], ['Relic Song', ['slp', 10]], ['Signal Beam', ['confusion', 10]], ['Ancient Power', ['self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10]], ['Steamroller', ['flinch', 30]], ['Bubble Beam', ['boosts spe: -1 ', 10]], ['Sludge', ['psn', 30]], ['Play Rough', ['boosts atk: -1 ', 10]], ['Astonish', ['flinch', 30]], ['Energy Ball', ['boosts spd: -1 ', 10]], ['Zen Headbutt', ['flinch', 20]], ['Iron Tail', ['boosts def: -1 ', 30]], ['Shadow Strike', ['boosts def: -1 ', 50]], ['Charge Beam', ['self boosts: spa: 1 ', 70]], ['Secret Power', ['par', 30]], ['Tri Attack', ['par frz or brn', 20]], ['Psychic', ['boosts spd: -1 ', 10]], ['Smog', ['psn', 40]], ['Steel Wing', ['self boosts: def: 1 ', 10]], ['Iron Head', ['flinch', 30]], ['Headbutt', ['flinch', 30]], ['Body Slam', ['par', 30]], ['Bug Buzz', ['boosts spd: -1 ', 10]], ['Seed Flare', ['boosts spd: -2 ', 40]], ['Mist Ball', ['boosts spa: -1 ', 50]], ['Earth Power', ['boosts spd: -1 ', 10]], ['Bolt Strike', ['par', 20]], ['Bite', ['flinch', 30]], ['Flamethrower', ['brn', 10]], ['Rock Climb', ['confusion', 20]], ['Freeze Shock', ['par', 30]], ['Dark Pulse', ['flinch', 20]], ['Flash Cannon', ['boosts spd: -1 ', 10]], ['Floaty Fall', ['flinch', 30]], ['Poison Fang', ['tox', 50]], ['Sludge Bomb', ['psn', 30]], ['Lick', ['par', 30]], ['Diamond Storm', ['self boosts: def: 2 ', 50]], ['Shadow Ball', ['boosts spd: -1 ', 20]], ['Cross Poison', ['psn', 10]], ['Sludge Wave', ['psn', 10]], ['Leaf Tornado', ['boosts accuracy: -1 ', 50]], ['Hyper Fang', ['flinch', 10]], ['Muddy Water', ['boosts accuracy: -1 ', 30]], ['Thunder', ['par', 30]], ['Constrict', ['boosts spe: -1 ', 10]], ['Stomp', ['flinch', 30]], ['Poison Tail', ['psn', 10]], ['Bone Club', ['flinch', 10]], ['Fire Blast', ['brn', 10]], ['Mud Bomb', ['boosts accuracy: -1 ', 30]], ['Twineedle', ['psn', 20]], ['Splishy Splash', ['par', 30]], ['Confusion', ['confusion', 10]], ['Steam Eruption', ['brn', 30]], ['Fiery Dance', ['self boosts: spa: 1 ', 50]], ['Night Daze', ['boosts accuracy: -1 ', 40]], ['Flare Blitz', ['brn', 10]], ['Mirror Shot', ['boosts accuracy: -1 ', 30]], ['Sacred Fire', ['brn', 50]], ['Ice Beam', ['frz', 10]], ['Poison Jab', ['psn', 30]], ['Double Iron Bash', ['flinch', 30]], ['Waterfall', ['flinch', 20]], ['Psybeam', ['confusion', 10]], ['Octazooka', ['boosts accuracy: -1 ', 50]], ['Spark', ['par', 30]], ['Needle Arm', ['flinch', 30]], ['Dragon Breath', ['par', 30]], ['Air Slash', ['flinch', 30]], ['Dragon Rush', ['flinch', 20]], ['Silver Wind', ['self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10]], ['Luster Purge', ['boosts spd: -1 ', 50]], ['Snore', ['flinch', 30]], ['Thunderbolt', ['par', 10]], ['Flame Wheel', ['brn', 10]], ['Bounce', ['par', 30]], ['Scald', ['brn', 30]], ['Force Palm', ['par', 30]], ['Hurricane', ['confusion', 30]], ['Ice Burn', ['brn', 30]], ['Gunk Shot', ['psn', 30]], ['Blaze Kick', ['brn', 10]], ['Lava Plume', ['brn', 30]], ['Meteor Mash', ['self boosts: atk: 1 ', 20]], ['Searing Shot', ['brn', 30]], ['Twister', ['flinch', 20]], ['Icicle Crash', ['flinch', 30]], ['Bubble', ['boosts spe: -1 ', 10]], ['Rock Smash', ['boosts def: -1 ', 50]], ['Volt Tackle', ['par', 10]], ['Ember', ['brn', 10]], ['Powder Snow', ['frz', 10]], ['Moonblast', ['boosts spa: -1 ', 30]], ['Rock Slide', ['flinch', 30]], ['Shadow Bone', ['boosts def: -1 ', 20]], ['Heat Wave', ['brn', 10]], ['Discharge', ['par', 30]], ['Ominous Wind', ['self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10]], ['Razor Shell', ['boosts def: -1 ', 50]], ['Rolling Kick', ['flinch', 30]], ['Blue Flare', ['brn', 20]], ['Sky Attack', ['flinch', 30]]])
    if move in moveswithsecondaryeffect.keys():
        try:
            attacker['luck']+=-moveswithsecondaryeffect[move][1]
            target['luck']+=moveswithsecondaryeffect[move][1]
            #check for secondary effect
            results=secondary_check(attacker,target,move,line,results,parsedlogfile)
        except:
            pass
    #check if weather
    if move in ['Sandstorm','Hail','Z-Sandstorm','Z-Hail','Max Rockfall','Max Hailstorm']:
        move=move.replace("Z-","").replace("Max Rockfall","Sandstorm").replace("Max Hailstorm","Hail")
        results['team1']['Sandstorm']=None
        results['team1']['Hail']=None
        results['team2']['Sandstorm']=None
        results['team2']['Hail']=None
        if attackingteam=="p1a":
            results['team2'][move]=attacker['nickname']
        elif attackingteam=="p2a":
            results['team1'][move]=attacker['nickname']
    #check future sight:
    if move in ["Future Sight","Doom Desire"]:
        if attackingteam=="p1a":
            results['team2'][move]=attacker['nickname']
        elif attackingteam=="p2a":
            results['team1'][move]=attacker['nickname']
    #check belly drum:
    if move.replace("Z-","") in ["Belly Drum","Clangorous Soul"]:
        turndata=list(filter(lambda x: x[1] == line[1] and x[0] > line[0], parsedlogfile))
        active=False
        for line_ in turndata:
            if (line_[2]=="setboost" and line_[3].find("[from] move: Belly Drum")>-1) or (line_[2]=="boost" and line_[3].find("|def|1")>-1):
                active=True
        for line_ in turndata:
            if line_[2]=="damage" and line_[3].find(attacker['nickname'])>-1 and active==True:
                healthremaining=int(line_[3].split("|",1)[1].split(" ",1)[0].split("/",1)[0].split("|",1)[0])
                priorhealth= attacker['remaininghealth']
                attacker['remaininghealth']=healthremaining
                attacker['hphealed']+=healthremaining-priorhealth
                break
            elif line_[2]=="heal" and line_[3].find(attacker['nickname'])>-1 and active==True:
                healthremaining=int(line_[3].split("|",1)[1].split(" ",1)[0].split("/",1)[0].split("|",1)[0])
                priorhealth=attacker['remaininghealth']
                attacker['remaininghealth']=healthremaining
                attacker['hphealed']+=healthremaining-priorhealth
                line_[2]="healprocessed"
    #check for suicide moves
    if move.replace("Z-","") in ['Final Gambit','Healing Wish',"Lunar Dance","Memento","Explosion","Self-Destruct"]:
        move=move.replace("Z-","")
        #search for miss 
        turndata=list(filter(lambda x: x[1] == line[1] and x[0] > line[0] , parsedlogfile))[::-1]
        miss=False
        for line in turndata:
            if (line[2]=="miss" and line[3].split(": ")[0]==attackingteam) or (line[2]=="immune" and line[3].split(": ")[0]==defendingteam):
                miss=True
        if miss==False or move in ['Healing Wish',"Lunar Dance","Explosion","Self-Destruct"]:
            attacker['deaths']+=1
            attacker['hphealed']+=-attacker['remaininghealth']
            attacker['remaininghealth']=0
            if attackingteam=="p1a":
                results['team1']['selfdeaths']+=1
            elif attackingteam=="p2a":
                results['team2']['selfdeaths']+=1
    #check for Perish Song
    if move=="Perish Song":
        results['Perish Song']=attacker['nickname']
    #check for court change
    if move=="Court Change":
        if results['team1']['Toxic Spikes']!=None:results['team2']['Toxic Spikes']=attacker['nickname']
        if results['team2']['Toxic Spikes']!=None:results['team1']['Toxic Spikes']=attacker['nickname']
        if results['team1']['Spikes']!=None:results['team2']['Spikes']=attacker['nickname']
        if results['team2']['Spikes']!=None:results['team1']['Spikes']=attacker['nickname']
        if results['team1']['Stealth Rock']!=None:results['team2']['Stealth Rock']=attacker['nickname']
        if results['team2']['Stealth Rock']!=None:results['team1']['Stealth Rock']=attacker['nickname'] 
    return line,parsedlogfile,results

def player_function(line,parsedlogfile,results):
    if line[3].split("|",1)[0]=="p1":
        results['team1']['coach']=line[3].split("|")[1]
    elif line[3].split("|",1)[0]=="p2":
        results['team2']['coach']=line[3].split("|")[1]
    return line,parsedlogfile,results

def poke_function(line,parsedlogfile,results):
    adjustedmon=line[3].split("|")[1].replace("-Mega-X","").replace("-Mega-Y","").replace("-Mega","")
    if line[3].split("|",1)[0]=="p1":
        results['team1']['roster'].append({
            'pokemon':line[3].split("|")[1], 'startform':adjustedmon,'nickname':adjustedmon,
            'kills':0,'deaths':0,'causeofdeath':None,'support':0,'damagedone':0,'hphealed':0,'luck':0,'remaininghealth':100,'lines':[],
            'confusion':None,'psn':None,'brn':None,'par':None,'frz':None,'tox':None,'Curse':None,
        })  
    elif line[3].split("|",1)[0]=="p2":
        results['team2']['roster'].append({
            'pokemon':line[3].split("|")[1], 'startform':adjustedmon,'nickname':adjustedmon,
            'kills':0,'deaths':0,'causeofdeath':None,'support':0,'damagedone':0,'hphealed':0,'luck':0,'remaininghealth':100,'lines':[],
            'confusion':None,'psn':None,'brn':None,'par':None,'frz':None,'tox':None,'Curse':None,
        })
    if adjustedmon in ['Zorua','Zoroark']:
        parsedlogfile=illusion_function(parsedlogfile,adjustedmon)
    return line,parsedlogfile,results

def replace_function(line,parsedlogfile,results):
    #replaceteam=line[3].split(": ")[0]
    #replacenickname=line[3].split("|")[0].split(": ",1)[1]
    #replacemon=line[3].split("|")[1]
    #mon=roster_search(replaceteam,replacemon,results)
    #if mon!=replacemon:
    #    mon['nickname']=replacenickname
    return line,parsedlogfile,results

def illusion_function(parsedlogfile,pokemon):
    replacelines=list(filter(lambda x: x[2]=="replace" and x[3].find(pokemon)>-1, parsedlogfile))
    for line_ in replacelines:
        replaceteam=line_[3].split(": ")[0]
        replacenickname=line_[3].split("|")[0].split(": ",1)[1]
        replacemon=line_[3].split("|")[1]
        relevantlines=list(filter(lambda x: x[0]<line_[0], parsedlogfile))[::-1]
        montoreplace=None
        for line in relevantlines:
            if line[3].find(replaceteam)>-1:
                montoreplace=line[3].split(f"{replaceteam}: ")[1].split("|")[0]
                break
        for line in relevantlines:
            if line[2] in ['switch','drag'] and line[3].find(montoreplace)>-1:
                monname=line[3].split("|")[1]
                line[3]=line[3].replace(f"{replaceteam}: {montoreplace}",f"{replaceteam}: {replacenickname}").replace(monname,pokemon)
                break
            else:
                line[3]=line[3].replace(f"{replaceteam}: {montoreplace}",f"{replaceteam}: {replacenickname}")
    return parsedlogfile

def sethp_function(line,parsedlogfile,results):
    if line[3].find("|[from] move: Pain Split")>-1 and len(line[3].split("|"))>4:
        targetteam=line[3].split(":",1)[0]
        target=line[3].split("|",1)[0].split(" ",1)[1]
        targethealth=int(line[3].split("|",1)[1].split("/")[0])
        attackingteam=line[3].split("|")[2].split(":",1)[0]
        attacker=line[3].split("|")[2].split(" ",1)[1]
        attackerhealth=int(line[3].split("|")[3].split("/")[0])
        #find mons
        target=roster_search(targetteam,target,results)
        attacker=roster_search(attackingteam,attacker,results)
        targetstarthealth=target['remaininghealth']
        attacherstarthealth=attacker['remaininghealth']
        target['remaininghealth']=targethealth
        attacker['remaininghealth']=attackerhealth
        damagedone=targetstarthealth-targethealth
        hphealed=attackerhealth-attacherstarthealth
        attacker['damagedone']+=damagedone
        attacker['hphealed']+=hphealed
    elif line[3].find("|[from] move: Pain Split")>-1:
        setmon=line[3].split("|")[0].split(": ")[1]
        setmonhealth=int(line[3].split("|")[1].split("/")[0])
        #look up move data
        turndata=list(filter(lambda x: x[1] == line[1] and x[0] < line[0] and x[2]=="move" , parsedlogfile))[::-1][0]
        targetteam=turndata[3].split("|")[2].split(": ",1)[0]
        target=turndata[3].split("|")[2].split(": ",1)[1]
        attackingteam=turndata[3].split(": ")[0]
        attacker=turndata[3].split("|")[0].split(": ",1)[1]
        target_=roster_search(targetteam,target,results)
        attacker_=roster_search(attackingteam,attacker,results)
        targetstarthealth=target_['remaininghealth']
        attacherstarthealth=attacker_['remaininghealth']
        if setmon==target:
            target_['remaininghealth']=setmonhealth
            damagedone=targetstarthealth-setmonhealth
            attacker_['damagedone']+=damagedone
        elif setmon==attacker:
            attacker_['remaininghealth']=setmonhealth
            hphealed=setmonhealth-attacherstarthealth
            attacker_['hphealed']+=hphealed  
    return line,parsedlogfile,results

def status_function(line,parsedlogfile,results):
    team=line[3].split(":",1)[0]
    if team=="p1a":
        team_='team1';otherteam="p2a"
    elif team=="p2a":
        team_='team2';otherteam="p1a"
    mon=line[3].split("|",1)[0].split(" ",1)[1]
    status=line[3].split("|")[1]
    mon=roster_search(team,mon,results)
    if line[3].find("[from] ability: ")>-1: 
        ability=line[3].split("|")[2].split("[from] ability: ")[1]
        mon['luck']+=-70
        activemon=line[3].split("|")[3].split(": ")[1]
        mon[status]=activemon
        activemon=roster_search(otherteam,activemon,results)
        activemon['luck']+=70
    elif line[3].find("[from] item: ")>-1: 
        matchdata=list(filter(lambda x: x[0] < line[0], parsedlogfile))[::-1]
        switched=False
        for line_ in matchdata:
            if line_[2]=="item" and line_[3].find(mon['nickname'])>-1:#and line_[3].find(cause.split(": ",1)[1])>-1
                switched=True
            if line_[2]=="move" and line_[3].split("|")[1] in ['Trick','Switcheroo'] and switched==True and line_[3].split("|")[0].split(": ",1)[1]!=mon['nickname']:
                damager=line_[3].split("|")[0].split(": ",1)[1]
                mon[status]=damager    
                break
            elif line_[2]=="move" and line_[3].split("|")[1] in ['Trick','Switcheroo'] and switched==True and line_[3].split("|")[0].split(": ",1)[1]==mon['nickname']:
                mon[status]=mon['nickname']
                break
        if switched==False:
            mon[status]=mon['nickname']
    else:
        movesthatcausestatus=dict([
            ['tox',['Toxic','Fling','Psycho Shift']],
            ['psn',['Toxic Thread','Poison Powder','Poison Gas','Baneful Bunker','Fling','Psycho Shift']],
            ['brn',['Beak Blast','Will-O-Wisp','Fling','Psycho Shift']],
            ['par',['Thunder Wave','Nuzzle','Glare','Stoked Sparksurfer','Stun Spore','Zap Cannon','Fling','Psycho Shift']],
            ['slp',['Spore','Sleep Powder','Dark Void','Grass Whistle','Hypnosis','Lovely Kiss','Sing','Psycho Shift']],
            ['frz',[]]
            ])
        statusmoves=movesthatcausestatus[status]
        turndata=list(filter(lambda x: x[1] == line[1] and x[0] < line[0], parsedlogfile))
        turndata=turndata[::-1]
        for line_ in turndata:
            if line_[2]=="move":
                move=line_[3].split("|")[1].replace("Z-","")
                attackingteam=line_[3].split(":",1)[0]
                attacker=line_[3].split("|",1)[0].split(" ",1)[1]
                if move in statusmoves and team!=attackingteam:
                    mon[status]=attacker
                    break
            elif line_[2]=="activate" and line_[3].find(f"|ability: Synchronize")>-1:
                mon[status]=line_[3].split("|")[0].split(": ",1)[1]
                break
        if (status=="psn" or status=="tox") and mon[status]==None and results[team_]['Toxic Spikes']!=None:
            mon[status]=results[team_]['Toxic Spikes']
    return line,parsedlogfile,results

def start_function(line,parsedlogfile,results):
    if line[3].find("|perish0")>-1:
        setter=results['Perish Song']
        team=line[3].split(": ",1)[0]
        mon=line[3].split("|")[0].split(": ",1)[1]
        mon_=roster_search(team,mon,results)
        mon_['deaths']=1
        priorhealth=mon_['remaininghealth']
        mon_['remaininghealth']=0
        if mon == setter:
            mon_['hphealed']+=-priorhealth
            if team=="p1a":
                results['team1']['selfdeaths']+=1
            elif team=="p2a":
                results['team2']['selfdeaths']+=1   
        else:
            if team=="p1a":
                setter=roster_search("p2a",setter,results)
            elif team=="p2a":
                setter=roster_search("p1a",setter,results)
            setter['damagedone']+=priorhealth
            setter['kills']+=1
    if line[3].split("|")[1]=="confusion":
        mon=line[3].split("|")[0].split(": ")[1]
        team=line[3].split(": ")[0]
        mon_=roster_search(team,mon,results)
        if line[3].find("[fatigue]")>-1:
            mon_['confusion']=mon
        else:
            turndata=list(filter(lambda x: x[0] < line[0] and x[1] == line[1] and x[2]=="move", parsedlogfile))[::-1]
            movesthatconfuse=['Dynamic Punch','Confuse Ray','Chatter','Supersonic']
            for line_ in turndata:
                move=line_[3].split("|")[1]
                team_=line_[3].split(": ")[0]
                attacker=line_[3].split("|")[0].split(": ")[1]
                if move in movesthatconfuse and team_!=team:
                    mon_['confusion']=attacker
            if mon_['confusion']==None:
                #check for berry
                turndata=list(filter(lambda x: x[0] < line[0] and x[1] == line[1] and x[2]=="enditem", parsedlogfile))[::-1]
                for line_ in turndata:
                    if line_[3].find("Berry")>-1:
                        mon_['confusion']=mon_['nickname']
    if line[3].split("|")[1]=="Curse":
        mon=line[3].split("|")[0].split(": ")[1]
        team=line[3].split(": ")[0]
        mon_=roster_search(team,mon,results)
        setter=line[3].split("|")[2].split(": ")[1]
        mon_['Curse']=setter
        turndata=list(filter(lambda x: x[0] > line[0] and x[1] == line[1] and x[2]=="damage", parsedlogfile))
        for line_ in turndata:
            team_=line_[3].split(": ")[0]
            if team_!=team:
                setter=roster_search(team_,setter,results)
                priorhealth=setter['remaininghealth']
                healthremaining=int(line_[3].split("|",1)[1].split(" ",1)[0].split("/",1)[0].split("|",1)[0])
                setter['remaininghealth']=healthremaining
                setter['hphealed']=healthremaining-priorhealth
                break
    return line,parsedlogfile,results

def switch_drag_function(line,parsedlogfile,results):
    if line[3].split(":",1)[0]=="p1a":
        results,line=namecheck(results,line,1)
    elif line[3].split(":",1)[0]=="p2a":
        results,line=namecheck(results,line,2)
    return line,parsedlogfile,results

def weather_function(line,parsedlogfile,results):
    if line[3].find("[from] ability: ")>-1:
        thisteam=line[3].split("[of] ")[1].split(":",1)[0]
        weather=line[3].split("|")[0]
        setter=line[3].split("|[of] ")[1].split(": ",1)[1]
        results['team1']['Sandstorm']=None
        results['team1']['Hail']=None
        results['team2']['Sandstorm']=None
        results['team2']['Hail']=None
        if weather in ['Sandstorm','Hail']:
            if thisteam=="p1a":
                results['team2'][weather]=setter
            elif thisteam=="p2a":
                results['team1'][weather]=setter
    elif line[3]=="none":
        results['team1']['Sandstorm']=None
        results['team1']['Hail']=None
        results['team2']['Sandstorm']=None
        results['team2']['Hail']=None
    return line,parsedlogfile,results
    
def win_function(line,parsedlogfile,results):
    winner=line[3]
    if winner==results['team1']['coach']:
        results['team1']['wins']=1
    elif winner==results['team2']['coach']:
        results['team2']['wins']=1
    return line,parsedlogfile,results

def zpower_function(line,parsedlogfile,results):
    if line[3].find("p1a")>-1:
        results['team1']['usedzmove']=True
    elif line[3].find("p2a")>-1:
        results['team2']['usedzmove']=True
    return line,parsedlogfile,results

def namecheck(results,line,teamnumber):
    nicknamesearch=line[3].split(" ",1)[1].split("|")
    healthremaining=int(line[3].split("|")[2].split("/",1)[0])
    if nicknamesearch[0]!=nicknamesearch[1] and nicknamesearch[1].find(f"{nicknamesearch[0]}-")==-1:
        if nicknamesearch[1].find("Silvally-")>-1:
            line[3]=line[3].replace(nicknamesearch[1],"Silvally")
            nicknamesearch[1]="Silvally"
        for item in results[f'team{teamnumber}']['roster']:
            if item['pokemon']==nicknamesearch[1]:
                item['nickname']=nicknamesearch[0]
                priorhealth=item['remaininghealth']
                item['hphealed']+=healthremaining-priorhealth
                item['remaininghealth']=healthremaining
    else:
        if nicknamesearch[1].find("Silvally-")>-1:
            line[3]=line[3].replace(nicknamesearch[1],"Silvally")
            nicknamesearch[1]="Silvally"
        for item in results[f'team{teamnumber}']['roster']:
            if item['pokemon']==nicknamesearch[1] and nicknamesearch[1].find("-Mega")==-1:
                item['startform']=nicknamesearch[0]
                item['nickname']=nicknamesearch[0]
                priorhealth=item['remaininghealth']
                item['hphealed']+=healthremaining-priorhealth
                item['remaininghealth']=healthremaining
    results[f'team{teamnumber}']['activemon']=nicknamesearch[0]
    if line[2]=="switch":    
        results[f'team{teamnumber}']['timesswitched']+=1
    return results,line

def replacemega(results,line,teamnumber):
    results[f'team{teamnumber}']['megaevolved']=True
    megasearch=line[3].split(" ",1)[1].split("|")
    for item in results[f'team{teamnumber}']['roster']:
        if item['pokemon']==megasearch[0] or item['nickname']==megasearch[0]:
            item['pokemon']=megasearch[1]
    return results,line

def initializeoutput():
    #initialize output json
    results={}
    results['team1']={}
    results['team2']={}
    results['team1']['coach']=""
    results['team2']['coach']=""
    results['team1']['roster']=[]
    results['team2']['roster']=[]
    results['team1']['wins']=0
    results['team2']['wins']=0
    results['team1']['forfeit']=0
    results['team2']['forfeit']=0
    results['team1']['score']=0
    results['team2']['score']=0
    results['team1']['megaevolved']=False
    results['team2']['megaevolved']=False
    results['team1']['usedzmove']=False
    results['team2']['usedzmove']=False
    results['team1']['timesswitched']=-1
    results['team2']['timesswitched']=-1
    results['team1']['selfdeaths']=0
    results['team2']['selfdeaths']=0
    results['team1']['remaininghealth']=0
    results['team2']['remaininghealth']=0
    results['team1']['totalhealth']=0
    results['team2']['totalhealth']=0
    results['team1']['kills']=0
    results['team2']['kills']=0
    results['team1']['deaths']=0
    results['team2']['deaths']=0
    results['team1']['luck']=0
    results['team2']['luck']=0
    results['team1']['damagedone']=0
    results['team2']['damagedone']=0
    results['team1']['hphealed']=0
    results['team2']['hphealed']=0
    results['team1']['support']=0
    results['team2']['support']=0
    results['team1']['activemon']=None
    results['team2']['activemon']=None
    results['team1']['Toxic Spikes']=None
    results['team2']['Toxic Spikes']=None
    results['team1']['Spikes']=None
    results['team2']['Spikes']=None
    results['team1']['Stealth Rock']=None
    results['team2']['Stealth Rock']=None
    results['team1']['Future Sight']=None
    results['team2']['Future Sight']=None
    results['team1']['Doom Desire']=None
    results['team2']['Doom Desire']=None
    results['team1']['Sandstorm']=None
    results['team2']['Sandstorm']=None
    results['team1']['Hail']=None
    results['team2']['Hail']=None
    results['team1']['Leech Seed']=None
    results['team2']['Leech Seed']=None
    results['Perish Song']=None
    results['numberofturns']=0
    results['turns']=[]
    results['replay']=""
    results['significantevents']=[]
    results['errormessage']=[]
    return results

def roster_search(team,pokemon,results):
    if team=="p1a":
        team="team1"
    elif team=="p2a":
        team="team2"
    if team=="p1":
        team="team1"
    elif team=="p2":
        team="team2"
    match=False
    for mon in results[team]['roster']:
        if mon['nickname']==pokemon:
            pokemon=mon
            match=True
            break
    if match==False:
        for mon in results[team]['roster']:
            if mon['nickname'].find(pokemon)>-1:
                pokemon=mon
                match=True
                break
    return pokemon

def alternativereplayparse(replay):
    #initialize variables
    logfile = requests.get(replay+".log").text.splitlines()
    parsedlogfile=[]
    line_number=0
    turn_number=0
    #initialize output json
    results=initializeoutput()
    results['replay']=replay
    #iterate through logfile
    for line in logfile:
        if line.find("|")>-1:
            #remove unneeded lines
            line=line.replace(", M","").replace(", F","").replace("-*","").replace(", shiny","").replace(", L50","").replace("-Super","").replace("-Large","").replace("-Small","").replace("-Blue","").replace("-Orange","").replace("Florges-White","Florges").replace("-Yellow","").replace("-Bug","").replace("-Dark","").replace("-Dragon","").replace("-Electric","").replace("-Fairy","").replace("-Fighting","").replace("-Fire","").replace("-Flying","").replace("-Ghost","").replace("-Grass","").replace("-Ground","").replace("-Ice","").replace("-Normal","").replace("-Poison","").replace("-Psychic","").replace("-Rock","").replace("-Steel","").replace("-Water","").replace("-Douse","").replace("-Burn","").replace("-Chill","").replace("-Shock","").replace("Type: ","Type:").replace("Mr. ","Mr.").replace("-Sensu","").replace("-Pom-Pom","").replace("-Pa'u","").replace("Farfetch'd","Farfetchd").replace("-Totem","").replace("-Resolute","").replace("-Meteor","").replace("Meowstic-F","Meowstic").replace("-East","").replace("Sirfetch'd","Sirfetchd")
            linestoremove=["|","|teampreview","|clearpoke","|upkeep"]
            badlines=["","|start","|player|p1","|player|p2","|player|p1|","|player|p2|","|-notarget","|-clearallboost","|-nothing"]
            linepurposestoremove=["j","c","l","teamsize","gen","gametype","tier","rule","-mega","seed","teampreview","anim"]
            linepurpose=line.split("|",2)[1].replace("-","")
            #iterate turn number
            if linepurpose=="turn":
                turn_number+=1
                results['numberofturns']=turn_number
            #add turn data
            elif line not in linestoremove and linepurpose not in linepurposestoremove and line not in badlines:
                lineremainder=line.split("|",2)[2]
                parsedlogfile.append([line_number,turn_number,linepurpose,lineremainder])
                line_number+=1
    #iterate through parsed logfile replacing names
    switchdraglines=list(filter(lambda x: x[2] in ["switch","drag"], parsedlogfile))[::-1]
    for line in switchdraglines:
        team=line[3].split(": ",)[0]
        nickname=line[3].split("|")[0].split(": ",)[1]
        pokemon=line[3].split("|")[1].split("-")[0]
        if pokemon.find(nickname)==-1:
            matchdata=list(filter(lambda x: x[0]>=line[0], parsedlogfile))
            for line_ in matchdata:
                line_[3]=line_[3].replace(nickname,pokemon)
    #iterate through parsed logfile
    for line in parsedlogfile:
        line,parsedlogfile,results=replay_parse_switch(line,parsedlogfile,results)
    #sort significant events
    results['significantevents']=sorted( results['significantevents'],key=lambda tup: tup[0])
    #update result totals
    teams=['team1','team2']
    categories=['kills','deaths','luck','support','hphealed','damagedone','remaininghealth']
    for team in teams:
        for mon in results[team]['roster']:
            results[team]['score']+=1-mon['deaths']
            for category in categories:
                results[team][category]+=mon[category]
                results[team][category]=round(results[team][category],2)
            mon['luck']= mon['luck']/100
            results[team]['totalhealth']+=100
        results[team]['luck']=results[team]['luck']/100
    #output results to json file
    with open('replayanalysis/NewParser/results.json', 'w') as f:
        json.dump(results,f,indent=2)
    #team1
    damagedone=results['team1']['damagedone']
    damagedonetest=results['team2']['totalhealth']-results['team2']['remaininghealth']+results['team2']['hphealed']
    score=results['team1']['score']
    scoretest=len(results['team1']['roster'])-results['team2']['kills']-results['team1']['selfdeaths']
    if damagedonetest!=damagedone: results['errormessage'].append("This replay's Team 1 damage numbers do not add up. Please contact claduva and do not submit the replay.")
    if scoretest!=score: results['errormessage'].append("This replay's Team 1 score numbers do not add up. Please contact claduva and do not submit the replay.")
    if score!=0 and results['team2']['wins']==1: results['errormessage'].append("The losing team's score should be 0. Please contact claduva and do not submit the replay.")
    #team2
    damagedone=results['team2']['damagedone']
    damagedonetest=results['team1']['totalhealth']-results['team1']['remaininghealth']+results['team1']['hphealed']
    score=results['team2']['score']
    scoretest=len(results['team2']['roster'])-results['team1']['kills']-results['team2']['selfdeaths']
    if damagedonetest!=damagedone: results['errormessage'].append("This replay's Team 2 damage numbers do not add up. Please contact claduva and do not submit the replay.")
    if scoretest!=score: results['errormessage'].append("This replay's Team 2 score numbers do not add up. Please contact claduva and do not submit the replay.")
    if score!=0 and results['team1']['wins']==1: results['errormessage'].append("The losing team's score should be 0. Please contact claduva and do not submit the replay.")
    return results