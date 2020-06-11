import requests
import json

from .luckfunctions import *

def replay_parse_switch(argument,parsedlogfile,results):
    switcher = {
        'activate': activate_function,
        'boost':boost_function,
        'cant': cant_function,
        'crit': crit_function,
        'curestatus': curestatus_function,
        'damage': damage_function,
        'detailschange': detailschange_function,
        'drag': switch_drag_function,
        'fieldstart': fieldstart_function,
        'fieldend': fieldend_function,
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
        'unboost': unboost_function,
        'weather': weather_function,
        'win': win_function,
        'zpower': zpower_function,
        #gen,turn,start,tie,detailschange,transform,formechange,switchout,faint,swap,move,cant,message,start,end,ability,endability,item,enditem,status,curestatus,cureteam,singleturn,singlemove,sidestart,sideend,weather,fieldstart,fieldend,sethp,message,hint,activate,heal,boost,unboost,setboost,swapboost,copyboost,clearboost,clearpositiveboost,clearnegativeboost,invertboost,clearallboost,crit,supereffective,resisted,block,fail,immune,miss,center,notarget,mega,primal,zpower,burst,zbroken,hitcount,waiting,anim
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument[2], lambda argument,parsedlogfile,results: (argument,parsedlogfile,results))
    # Execute the function
    return func(argument,parsedlogfile,results)

def alternate_replay_parse_switch(argument,parsedlogfile,results):
    switcher = {
        'activate': activate_function,
        'boost':boost_function,
        'cant': cant_function,
        'crit': crit_function,
        'curestatus': curestatus_function,
        'damage': damage_function,
        'detailschange': detailschange_function,
        'drag': switch_drag_function,
        'fieldstart': fieldstart_function,
        'fieldend': fieldend_function,
        'heal':heal_function,
        'message': message_function,
        'move': move_function,
        'player': player_function,
        'poke': poke_function,
        'replace': replace_function,
        'sethp':sethp_function,
        'start': start_function,
        'status': status_function,
        'switch': alternate_switch_drag_function,
        'unboost': unboost_function,
        'weather': weather_function,
        'win': win_function,
        'zpower': zpower_function,
        #gen,turn,start,tie,detailschange,transform,formechange,switchout,faint,swap,move,cant,message,start,end,ability,endability,item,enditem,status,curestatus,cureteam,singleturn,singlemove,sidestart,sideend,weather,fieldstart,fieldend,sethp,message,hint,activate,heal,boost,unboost,setboost,swapboost,copyboost,clearboost,clearpositiveboost,clearnegativeboost,invertboost,clearallboost,crit,supereffective,resisted,block,fail,immune,miss,center,notarget,mega,primal,zpower,burst,zbroken,hitcount,waiting,anim
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument[2], lambda argument,parsedlogfile,results: (argument,parsedlogfile,results))
    # Execute the function
    return func(argument,parsedlogfile,results)

def prepare_parsedlogfile(logfile,replay):
    parsedlogfile=[]
    line_number=0
    turn_number=0
    results=initializeoutput()
    results['replay']=replay 
    for line in logfile:
        if line.find("|")>-1:
            #remove unneeded lines
            line=line.replace(", M","").replace(", F","").replace("-*","").replace(", shiny","").replace(", L50","").replace(", L5","").replace("-Striped","").replace("-Trash","").replace("-Sandy","").replace("Indeedee-F","Indeedee").replace("-Super","").replace("-Large","").replace("-Small","").replace("-Blue","").replace("-Orange","").replace("Florges-White","Florges").replace("-Pokeball","").replace("-Elegant","").replace("-Indigo","").replace("-Yellow","").replace("-Bug","").replace("-Dark","").replace("-Dragon","").replace("-Electric","").replace("-Fairy","").replace("-Fighting","").replace("-Fire","").replace("-Flying","").replace("-Ghost","").replace("-Grass","").replace("-Ground","").replace("-Ice","").replace("-Normal","").replace("-Poison","").replace("-Psychic","").replace("-Rock","").replace("-Steel","").replace("-Water","").replace("-Douse","").replace("-Burn","").replace("-Chill","").replace("-Shock","").replace("Type: ","Type:").replace("Mr. ","Mr.").replace("-Sensu","").replace("-Pom-Pom","").replace("-Pa'u","").replace("Farfetch'd","Farfetchd").replace("-Totem","").replace("-Resolute","").replace("-Meteor","").replace("Meowstic-F","Meowstic").replace("-East","").replace("fetch’d","fetchd").replace("fetch'd","fetchd").replace("-Ruby-Cream","").replace("-Matcha-Cream","").replace("-Mint-Cream","").replace("-Lemon-Cream","").replace("-Salted-Cream","").replace("-Ruby-Swirl","").replace("-Caramel-Swirl","").replace("-Rainbow-Swirl","")
            linestoremove=["|","|teampreview","|clearpoke","|upkeep"]
            badlines=["","|start","|player|p1","|player|p2","|player|p1|","|player|p2|","|-notarget","|-clearallboost","|-nothing","|-ohko","|rated"]
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
    return results,parsedlogfile

def newreplayparse(replay):
    #initialize variables
    if replay.find("logfiles")>-1 and replay.find(".txt")>-1:
        logfile = requests.get(replay).text.splitlines()
    else:
        logfile = requests.get(replay+".log").text.splitlines()   
    #iterate through parsed logfile
    try:
        results,parsedlogfile=prepare_parsedlogfile(logfile,replay)
        for line in parsedlogfile:
            line,parsedlogfile,results=alternate_replay_parse_switch(line,parsedlogfile,results)
    except:
        results,parsedlogfile=prepare_parsedlogfile(logfile,replay)
        for line in parsedlogfile:
            line,parsedlogfile,results=replay_parse_switch(line,parsedlogfile,results)
    #sort significant events
    results['significantevents']=sorted( results['significantevents'],key=lambda tup: tup[0])
    #sort luckcatalog
    results['luckcatalog']=sorted( results['luckcatalog'],key=lambda tup: tup[1])
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

def luckappend(line,results,mon,event,luckchange):
    startluck=mon['luck']/100
    mon['luck']+=luckchange
    if luckchange!=0:
        results['luckcatalog'].append([line[1],mon['pokemon'],event,startluck,luckchange/100,mon['luck']/100])
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
        results=luckappend(line,results,attacker,f"Mon is confused",-33)
        results=luckappend(line,results,defender,f"Opponent is confused",33)
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

def boost_function(line,parsedlogfile,results):
    team=line[3].split(":")[0]
    mon=line[3].split(": ")[1].split("|")[0]
    stat=line[3].split("|")[1]
    boostnum=int(line[3].split("|")[2])
    mon=roster_search(team,mon,results)
    mon[stat]+=boostnum
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
        results=luckappend(line,results,pokemon,f"Mon Could Not Move Due to Freeze",-20)
        results=luckappend(line,results,activemon,f"Opponent Could Not Move Due to Freeze",20)
    elif reason=="par":
        results=luckappend(line,results,pokemon,f"Mon Could Not Move Due to Paralysis",-75)
        results=luckappend(line,results,activemon,f"Opponent Could Not Move Due to Paralysis",75)
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
        if cause=="spikes": cause='Spikes'
        damager=None ;move=None
        if cause=="psn" and pokemon[cause]==None:
            cause="tox"
        if cause in ['Stealth Rock','Spikes','G-Max Steelsurge']:
            damager=roster_search(otherteam,results[thisteam][cause],results)
        elif cause.title() in ['Sandstorm','Hail']:
            if results[thisteam][cause.title()]!=None:
                damager=roster_search(otherteam,results[thisteam][cause.title()],results)
            elif results[otherteam_][cause.title()]!=None:
                setter=roster_search(team,results[otherteam_][cause.title()],results)
                setter['hphealed']+=-damagedone
        elif cause.find("item: Rocky Helmet")>-1 or cause.find("Leech Seed")>-1 or cause.find("ability: Iron Barbs")>-1 or cause.find("ability: Rough Skin")>-1 or cause.find("ability: Aftermath")>-1 or cause.find("ability: Liquid Ooze")>-1 or cause.find("ability: Innards Out")>-1 or cause.find("ability: Bad Dreams")>-1 or cause.find("ability: Gulp Missile")>-1  or cause.find("Spiky Shield")>-1 or cause.find("leechseed")>-1:
            damager=cause.split("|[of] ")[1].split(": ",1)[1]
            team=cause.split("|[of] ")[1].split(": ",1)[0]
            damager=roster_search(team,damager,results)
        elif cause.find("move: Whirlpool")>-1 or cause.find("move: Infestation")>-1 or cause.find("move: Magma Storm")>-1 or cause.find("move: Wrap")>-1 or cause.find("move: Fire Spin")>-1 or cause.find("move: Sand Tomb")>-1 or cause.find("ability: Disguise|[of]")>-1 or cause.find("mimikyubusted")>-1 or cause.find("Mimikyu-Busted")>-1:
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
            #results['significantevents'].append([line[1],f"LUCK: {pokemon['pokemon']} hit itself in confusion caused by {pokemon['confusion']}."])
            results=luckappend(line,results,pokemon,f"Mon Hit Self In Confusion",-100)
            results=luckappend(line,results,activeopponent,f"Opponent Hit Self In Confusion",100)
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

def fieldstart_function(line,parsedlogfile,results):
    if line[3].find("Gravity")>-1:
        results['Gravity']=1.667
    return line,parsedlogfile,results

def fieldend_function(line,parsedlogfile,results):
    if line[3].find("Gravity")>-1:
        results['Gravity']=1.0
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
    #append to movelist
    if move in attacker['moves']:
        attacker['moves'][move]['uses']+=1
        attacker['moves'][move]['hits']+=1
    else:
        attacker['moves'][move]={
            'uses':1,
            'hits':1,
            'crits':0,
            'posssecondaryeffects':0,
            'secondaryeffects':0,
        }
    #check for 2 turn moves
    if line[3].find("[still]")>-1:
        if move in ['Fly','Dive','Bounce','Dig','Sky Drop','Shadow Force','Phantom Force']:
            attacker['semiinv']=True
        if move not in ['Scald']:   
            return line,parsedlogfile,results
        else:
            try:
                if attackingteam=="p1a":
                    defendingteam='p2a'
                    target=roster_search(defendingteam,results['team2']['activemon'],results)
                elif attackingteam=="p2a":
                    defendingteam='p1a'
                    target=roster_search(defendingteam,results['team1']['activemon'],results)
            except:
                defendingteam=None; target=None
    if move in ['Fly','Dive','Bounce','Dig','Sky Drop','Shadow Force','Phantom Force']:
        attacker['semiinv']=False
    try:
        semiinv=target['semiinv']
    except:
        semiinv=False
    #check if paralyzed or frozen
    if attackingteam=="p1a":
        opponent=results['team2']['activemon']
        opponent=roster_search('p2a',opponent,results)
    elif attackingteam=="p2a":
        opponent=results['team1']['activemon']
        opponent=roster_search('p1a',opponent,results)
    if attacker['par']!=None:
        results=luckappend(line,results,attacker,f"Mon Broke Through Paralysis",25)
        results=luckappend(line,results,opponent,f"Opponent Broke Through Paralysis",-25)
    if attacker['frz']!=None:
        results=luckappend(line,results,attacker,f"Mon Thawed",80)
        attacker['frz']=None
        results=luckappend(line,results,opponent,f"Opponent Thawed",-80)
    #check for immunity
    turndata=list(filter(lambda x: x[1] == line[1] and x[0] > line[0], parsedlogfile))
    turndata_=list(filter(lambda x: x[1] == line[1] and x[0] < line[0], parsedlogfile))
    notimmune=True
    targetalive=True
    movedfirst=True
    targetnotprotected=True
    if line[3].find("[notarget]")>-1:
        targetmon=False
    else:
        targetmon=True
    try:
        for line_ in turndata:
            if line_[2]=="immune" and line_[3].find(defendingteam)>-1 and line_[3].find(target['nickname'])>-1:
                notimmune=False
            if line_[2]=="ability" and line_[3].find(defendingteam)>-1 and line_[3].find(target['nickname'])>-1 and line_[3].split("|")[2] in ['Storm Drain','Lightning Rod','Sap Sipper','Flash Fire','Motor Drive']:
                notimmune=False
            if line_[2]=="damage" and line_[3].find(defendingteam)>-1 and line_[3].find(target['nickname'])>-1 and line_[3].find("|0 fnt")>-1 and line_[3].find("[from]")==-1:
                targetalive=False
            if line_[2]=="activate" and line_[3].find(defendingteam)>-1 and line_[3].find(target['nickname'])>-1 and line_[3].split("|")[1].split("move: ")[1] in ['Protect','Detect',"King's Sheild",'Spiky Sheild','Mat Block','Obstruct']:
                targetnotprotected=False
            if line_[2] in ['switch','drag'] and line_[3].find(attackingteam)>-1:
                break
        for line_ in turndata_:
            if line_[2] in ["move","switch"] and line_[3].split(": ")[0]==defendingteam:
                movedfirst=False
    except:
        pass
    #support moves
    supportmoves=['Reflect','Light Screen','Heal Bell','Aromatherapy','Wish','Stealth Rock','Spikes','Toxic Spikes','Sticky Web', 'Aurora Veil','Defog','Rapid Spin','Hail','Sandstorm','Sunny Day','Rain Dance','Encore','Taunt','Haze','Clear Smog','Roar','Whirlwind','Leech Seed','Toxic','Will-O-Wisp','Stun Spore','Poison Powder','Block','Mean Look','Dark Void','Destiny Bond','Disable','Electric Terrain','Embargo','Endure','Fairy Lock',"Forest's Curse",'Glare','Grass Whistle','Grassy Terrain','Gravity','Grudge','Heal Block','Healing Wish','Hypnosis','Lucky Chant','Lunar Dance','Magic Coat','Magic Room','Mean Look','Memento','Mist','Misty Terrain','Mud Sport','Parting Shot','Perish Song','Poison Gas','Psychic Terrain','Safeguard','Simple Beam','Sing','Skill Swap','Sleep Powder','Soak','Speed Swap','Spider Web','Spite','Spore','Sweet Kiss','Switcheroo','Tailwind','Thunder Wave','Torment','Toxic Thread','Trick','Trick Room','Water Sport','Wonder Room','Worry Seed','Yawn']
    #check for support
    if move in supportmoves:
        attacker['support']+=1
        results['significantevents'].append([line[1],f"{attacker['pokemon']} provided support by using {move}"])
    #check for hazards
    hazardmoves=["Stealth Rock","Spikes","Toxic Spikes","G-Max Steelsurge"]
    if move in hazardmoves:
        if attackingteam=="p1a":
            results['team2'][move]=attacker['nickname']
        elif attackingteam=="p2a":
            results['team1'][move]=attacker['nickname']
    #moves that can miss
    #movesthatcanmiss=dict([['Precipice Blades', 85], ['High Horsepower', 95], ['Sand Tomb', 85], ['Triple Kick', 90], ['Tail Slap', 85], ['Double Slap', 85], ['Sky Uppercut', 90], ['Super Fang', 90], ['Hyper Beam', 90], ['Dynamic Punch', 50], ['Focus Blast', 70], ['Ice Ball', 90], ['Crush Claw', 95], ['Leech Seed', 90], ['Metal Claw', 95], ['Magma Storm', 75], ['Aeroblast', 95], ['Thunder Wave', 90], ['Head Smash', 80], ['Sing', 55], ['Blizzard', 70], ['Blast Burn', 90], ['Pin Missile', 95], ['Overheat', 90], ['Swagger', 85], ['Flying Press', 95], ['Fly', 95], ['Poison Gas', 90], ['Crabhammer', 90], ['Razor Leaf', 95], ['Poison Powder', 75], ['Rock Tomb', 95], ['Power Whip', 85], ['Supersonic', 55], ['Bind', 85], ['Fissure', 30], ['Sweet Kiss', 75], ['Play Rough', 90], ['Fury Swipes', 80], ['Zen Headbutt', 90], ['Belch', 90], ['Fury Cutter', 95], ['Iron Tail', 75], ['Toxic', 90], ['Egg Bomb', 75], ['Shadow Strike', 95], ['Thunder Fang', 95], ['Charge Beam', 90], ['Lovely Kiss', 75], ['Clamp', 85], ['Rock Throw', 90], ['Ice Fang', 95], ['Electroweb', 95], ['Whirlpool', 85], ['Smog', 70], ['Icy Wind', 95], ['Steel Wing', 90], ['Sonic Boom', 90], ['Hypnosis', 60], ['Fire Fang', 95], ['Seed Flare', 85], ['Hydro Cannon', 90], ['Jump Kick', 95], ['Leaf Storm', 90], ['Bolt Strike', 85], ['Air Cutter', 95], ['Mega Kick', 75], ['Inferno', 50], ['Rock Climb', 85], ['Rock Blast', 90], ['Freeze Shock', 90], ['Drill Run', 95], ['Floaty Fall', 95], ['Fire Spin', 85], ['Frenzy Plant', 90], ['Bone Rush', 90], ['Guillotine', 30], ['Slam', 75], ['Aqua Tail', 90], ['Diamond Storm', 95], ['Metal Sound', 85], ['Psycho Boost', 90], ['Gear Grind', 85], ['Barrage', 85], ['Bonemerang', 90], ['Draco Meteor', 90], ['Leaf Tornado', 90], ['Hyper Fang', 90], ['Muddy Water', 85], ['Thunder', 70], ['Sleep Powder', 75], ['Hammer Arm', 90], ['Origin Pulse', 85], ['Kinesis', 80], ['Grass Whistle', 55], ['Bone Club', 85], ['Fire Blast', 85], ['Mud Bomb', 85], ['Sheer Cold', 30], ['Frost Breath', 90], ['Roar of Time', 90], ['Hydro Pump', 80], ['Fury Attack', 85], ['High Jump Kick', 90], ['Steam Eruption', 95], ['Mega Punch', 85], ['Stun Spore', 75], ['Night Daze', 95], ['Dragon Tail', 90], ['Horn Drill', 30], ['String Shot', 95], ['Ice Hammer', 90], ['V-create', 95], ['Mud Shot', 95], ['Present', 90], ['Mirror Shot', 85], ['Megahorn', 85], ['Screech', 85], ['Sacred Fire', 95], ['Take Down', 85], ['Zap Cannon', 50], ['Octazooka', 85], ['Double Hit', 90], ['Snarl', 95], ['Stone Edge', 80], ['Rock Wrecker', 90], ['Cut', 95], ['Comet Punch', 85], ['Air Slash', 95], ['Fleur Cannon', 90], ['Dragon Rush', 75], ['Submission', 80], ['Circle Throw', 90], ['Bounce', 85], ['Giga Impact', 90], ['Hurricane', 70], ['Ice Burn', 90], ['Cross Chop', 80], ['Gunk Shot', 80], ['Blaze Kick', 90], ['Meteor Mash', 90], ['Dark Void', 50], ['Dual Chop', 90], ['Rollout', 90], ['Wrap', 90], ['Icicle Crash', 90], ['Will-O-Wisp', 85], ['Glaciate', 95], ['Spacial Rend', 95], ['Light of Ruin', 90], ["Nature's Madness", 90], ['Rock Slide', 90], ['Heat Wave', 90], ['Razor Shell', 95], ['Rolling Kick', 85], ['Blue Flare', 85], ['Sky Attack', 90]])
    movesthatcanmiss1=[['Eerie Impulse', 100], ['Scratch', 100], ['Anchor Shot', 100], ['Avalanche', 100], ['Sand Tomb', 85], ['Fire Punch', 100], ['Infestation', 100], ['Superpower', 100], ['Zing Zap', 100], ['Giga Drain', 100], ['Chatter', 100], ['Ice Punch', 100], ['Tail Slap', 85], ['Double Slap', 85], ['Thunder Shock', 100], ['Sky Uppercut', 90], ['Super Fang', 90], ['Hyper Beam', 90], ['Dynamic Punch', 50], ['Poison Sting', 100], ['Dig', 100], ['Focus Blast', 70], ['Liquidation', 100], ['Double Kick', 100], ['Ice Ball', 90], ['Round', 100], ['False Swipe', 100], ['Crush Claw', 95], ['Leech Seed', 90], ['Shadow Sneak', 100], ['Crush Grip', 100], ['Hidden Power Electric', 100], ['Seed Bomb', 100], ['Hidden Power Fire', 100], ['Chip Away', 100], ['Metal Claw', 95], ['Feather Dance', 100], ['Acid', 100], ['Baddy Bad', 100], ['Accelerock', 100], ['Aurora Beam', 100], ['Heart Stamp', 100], ['Magma Storm', 75], ['Crunch', 100], ['Aeroblast', 95], ['Explosion', 100], ['Thunder Wave', 90], ['Moongeist Beam', 100], ['Revenge', 100], ['Wake-Up Slap', 100], ['Pursuit', 100], ['Head Smash', 80], ['Sing', 55], ['Earthquake', 100], ['Gastro Acid', 100], ['Incinerate', 100], ['Water Pulse', 100], ['Dragon Pulse', 100], ['Glitzy Glow', 100], ['Acid Spray', 100], ['Thunder Punch', 100], ['Extrasensory', 100], ['Wring Out', 100], ["Forest's Curse", 100], ['Blizzard', 70], ['Blast Burn', 90], ['Paleo Wave', 100], ['Mud-Slap', 100], ['Freeze-Dry', 100], ['Heavy Slam', 100], ['Overheat', 90], ['Captivate', 100], ['Flame Charge', 100], ['Swagger', 85], ['Dizzy Punch', 100], ['Flying Press', 95], ['Lunge', 100], ['Prismatic Laser', 100], ['U-turn', 100], ['Future Sight', 100], ['Fire Lash', 100], ['Smelling Salts', 100], ['Burn Up', 100], ['Bug Bite', 100], ['Poison Gas', 90], ['Hidden Power Ghost', 100], ['Shell Trap', 100], ['Attract', 100], ['Sky Drop', 100], ['Crabhammer', 90], ['Darkest Lariat', 100], ['Hidden Power', 100], ['Razor Leaf', 95], ['Poison Powder', 75], ['Head Charge', 100], ['Dive', 100], ['Signal Beam', 100], ['Rock Tomb', 95], ['Power Whip', 85], ['Buzzy Buzz', 100], ['Supersonic', 55], ['Psychic Fangs', 100], ['Bind', 85], ['Counter', 100], ['Memento', 100], ['Throat Chop', 100], ['Parabolic Charge', 100], ['Retaliate', 100], ['Final Gambit', 100], ['Steamroller', 100], ['Bullet Seed', 100], ['Freezy Frost', 100], ['Reversal', 100], ['Aqua Jet', 100], ['Grass Knot', 100], ['Fissure', 30], ['Flame Burst', 100], ['Thief', 100], ['Sweet Kiss', 75], ['Astonish', 100], ['Dream Eater', 100], ['Energy Ball', 100], ['Fury Swipes', 80], ['Return', 100], ['Fling', 100], ['Belch', 90], ['Power Trip', 100], ['Fury Cutter', 95], ['Iron Tail', 75], ['Toxic', 90], ['Hidden Power Flying', 100], ['Egg Bomb', 75], ['Payback', 100], ['Fusion Flare', 100], ['Flail', 100], ['Boomburst', 100], ['Secret Sword', 100], ['Thunder Fang', 95], ['Charge Beam', 90], ['Lovely Kiss', 75], ['Rapid Spin', 100], ['Skull Bash', 100], ['Clamp', 85], ['Rock Throw', 90], ['Secret Power', 100], ['Fairy Wind', 100], ['Water Shuriken', 100], ['Struggle Bug', 100], ['Ice Fang', 95], ['Self-Destruct', 100], ['Teeter Dance', 100], ['Stored Power', 100], ['Tri Attack', 100], ['Psychic', 100], ['Electroweb', 95], ['Weather Ball', 100], ['Whirlpool', 85], ['Smog', 70], ['Baby-Doll Eyes', 100], ['Assurance', 100], ['Icy Wind', 95], ['Steel Wing', 90], ['Core Enforcer', 100], ['Synchronoise', 100], ['Zippy Zap', 100], ['Petal Dance', 100], ['Iron Head', 100], ['Sonic Boom', 90], ['Trop Kick', 100], ['Headbutt', 100], ['Drain Punch', 100], ['Hypnosis', 60], ['Dragon Rage', 100], ['Bug Buzz', 100], ['Cotton Spore', 100], ['Fire Fang', 95], ['Sludge', 100], ['Mist Ball', 100], ['Jump Kick', 95], ['Water Spout', 100], ['Ice Shard', 100], ['Earth Power', 100], ['Stomping Tantrum', 100], ['Bolt Strike', 85], ['Bite', 100], ['Sappy Seed', 100], ['Mega Kick', 75], ['Inferno', 50], ['Confuse Ray', 100], ['Rock Climb', 85], ['Rock Blast', 90], ['Feint', 100], ['Sucker Punch', 100], ['Dragon Ascent', 100], ['Freeze Shock', 90], ['Peck', 100], ['Psywave', 100], ['Drill Run', 95], ['Leafage', 100], ['Dark Pulse', 100], ['Flash Cannon', 100], ['Floaty Fall', 95], ['Poison Fang', 100], ['Dazzling Gleam', 100], ['Double-Edge', 100], ['Hidden Power Rock', 100], ['Encore', 100], ['Sweet Scent', 100], ['Sludge Bomb', 100], ['Lick', 100], ['Fire Spin', 85], ['Close Combat', 100], ['Bone Rush', 90], ['Guillotine', 30], ['Slam', 75], ['Torment', 100], ['Aqua Tail', 90], ['Strength', 100], ['Soak', 100], ['Fusion Bolt', 100], ['Rage', 100], ['Hidden Power Dark', 100], ['Metal Sound', 85], ['Gyro Ball', 100], ['Psycho Boost', 90], ['Surf', 100], ['Taunt', 100], ['Gear Grind', 85], ['Shadow Ball', 100], ['Eruption', 100], ['Barrage', 85], ['Charm', 100], ['Shadow Force', 100], ['Bonemerang', 90], ['Cross Poison', 100], ['Low Sweep', 100], ['Sludge Wave', 100], ['Leaf Tornado', 90], ['Hyper Fang', 90], ['Covet', 100], ['Karate Chop', 100], ['Fell Stinger', 100], ['Thunder', 70], ['Constrict', 100], ['Razor Wind', 100], ['Water Pledge', 100], ['Brine', 100], ['Hammer Arm', 90], ['Last Resort', 100], ['Bullet Punch', 100], ['Spite', 100], ['Brick Break', 100], ['Pay Day', 100], ['Switcheroo', 100], ['Oblivion Wing', 100], ['Origin Pulse', 85], ['Kinesis', 80], ['Stomp', 100], ['Grass Whistle', 55], ['Poison Tail', 100], ['Bone Club', 85], ['Fire Blast', 85], ['Brave Bird', 100], ['Gust', 100], ['Heat Crash', 100], ['Sand Attack', 100], ['Mud Bomb', 85], ['Beat Up', 100], ['Leaf Blade', 100], ['Spore', 100], ['Sparkly Swirl', 100], ['Trick', 100], ['Powder', 100], ['Twineedle', 100], ['Solar Blade', 100], ['Splishy Splash', 100], ['Spirit Shackle', 100], ['Nightmare', 100], ['Parting Shot', 100], ['Mystical Fire', 100], ['Confusion', 100], ['Pluck', 100], ['Frost Breath', 90], ['Roar of Time', 90], ['Fury Attack', 85], ['High Jump Kick', 90], ['Brutal Swing', 100], ['Petal Blizzard', 100], ['Wing Attack', 100], ['Hidden Power Steel', 100], ['Wood Hammer', 100], ['Hidden Power Water', 100], ['Fiery Dance', 100], ['Echoed Voice', 100], ['Smack Down', 100], ["Land's Wrath", 100], ['Mega Punch', 85], ['Stun Spore', 75], ['Revelation Dance', 100], ['Night Daze', 95], ['Scary Face', 100], ['Dragon Tail', 90], ['Horn Drill', 30], ['String Shot', 95], ['Flare Blitz', 100], ['Heal Block', 100], ['Ice Hammer', 90], ['V-create', 95], ['Screech', 85], ['Shadow Claw', 100], ['Sacred Fire', 95], ['Ice Beam', 100], ['Facade', 100], ['Worry Seed', 100], ['Vice Grip', 100], ['Growl', 100], ['Hidden Power Ice', 100], ['Extreme Speed', 100], ['Poison Jab', 100], ['Take Down', 85], ['Phantom Force', 100], ['Double Iron Bash', 100], ['Mind Blown', 100], ['Multi-Attack', 100], ['Zap Cannon', 50], ['Absorb', 100], ['Waterfall', 100], ['Judgment', 100], ['Hidden Power Bug', 100], ['Psybeam', 100], ['Knock Off', 100], ['Octazooka', 85], ['Hyper Voice', 100], ['Double Hit', 90], ['Spark', 100], ['Stone Edge', 80], ['Metal Burst', 100], ['Rock Wrecker', 90], ['Bouncy Bubble', 100], ['Draining Kiss', 100], ['Mud Shot', 95], ['Present', 90], ['Mirror Shot', 85], ['Megahorn', 85], ['Acrobatics', 100], ['Fleur Cannon', 90], ['Dragon Rush', 75], ['Solar Beam', 100], ['Mach Punch', 100], ['Luster Purge', 100], ['Snore', 100], ['Submission', 80], ['Vacuum Wave', 100], ['Thunderbolt', 100], ['Circle Throw', 90], ['Flame Wheel', 100], ['Hidden Power Poison', 100], ['Glare', 100], ['Flatter', 100], ['Fire Pledge', 100], ['Bounce', 85], ['Photon Geyser', 100], ['Giga Impact', 90], ['Dragon Claw', 100], ['Endeavor', 100], ['Scald', 100], ['Uproar', 100], ['Force Palm', 100], ['Hurricane', 70], ['Ice Burn', 90], ['Magnitude', 100], ['Cross Chop', 80], ['Psyshock', 100], ['Hidden Power Grass', 100], ['Techno Blast', 100], ['Gunk Shot', 80], ['Wild Charge', 100], ['Dragon Hammer', 100], ['Horn Attack', 100], ['Noble Roar', 100], ['Blaze Kick', 90], ['Psystrike', 100], ['Spike Cannon', 100], ['Horn Leech', 100], ['Searing Shot', 100], ['Dark Void', 50], ['Arm Thrust', 100], ['Dual Chop', 90], ['Foul Play', 100], ['Twister', 100], ['Focus Punch', 100], ['Slash', 100], ['Rollout', 90], ['Icicle Spear', 100], ['Wrap', 90], ['Leech Life', 100], ['Sacred Sword', 100], ['Hex', 100], ['Spit Up', 100], ['Will-O-Wisp', 85], ['Bubble', 100], ['Quick Attack', 100], ['Glaciate', 95], ['Night Shade', 100], ['Psycho Cut', 100], ['Sizzly Slide', 100], ['Rock Smash', 100], ['Volt Tackle', 100], ['Grass Pledge', 100], ['Sparkling Aria', 100], ['Embargo', 100], ['Vine Whip', 100], ['Ember', 100], ['Spacial Rend', 95], ['Tail Whip', 100], ['Light of Ruin', 90], ['Powder Snow', 100], ['Power-Up Punch', 100], ['Spectral Thief', 100], ['Smokescreen', 100], ['Moonblast', 100], ['Leer', 100], ['Thousand Waves', 100], ['Rock Slide', 90], ['Drill Peck', 100], ['Storm Throw', 100], ['Heat Wave', 90], ['Mirror Coat', 100], ['Tackle', 100], ['Discharge', 100], ['Strength Sap', 100], ['Razor Shell', 95], ['Hidden Power Ground', 100], ['Rolling Kick', 85], ['Blue Flare', 85], ['Sky Attack', 90], ['Power Gem', 100], ['Mega Drain', 100], ['High Horsepower', 95], ['Seismic Toss', 100], ['Electro Ball', 100], ['Flash', 100], ['Tickle', 100], ['Quash', 100], ['Venom Drench', 100], ['Pollen Puff', 100], ['Triple Kick', 90], ['Night Slash', 100], ['Plasma Fists', 100], ['Punishment', 100], ['Pin Missile', 95], ['First Impression', 100], ['Fly', 95], ['Natural Gift', 100], ['Relic Song', 100], ['Fake Out', 100], ['Disable', 100], ['Ancient Power', 100], ['Bubble Beam', 100], ['Play Rough', 90], ['Zen Headbutt', 90], ['Clanging Scales', 100], ['Shadow Strike', 95], ['Hidden Power Dragon', 100], ['Body Slam', 100], ['Seed Flare', 85], ['Leaf Storm', 90], ['Air Cutter', 95], ['Flamethrower', 100], ['Doom Desire', 100], ['Sunsteel Strike', 100], ['Frenzy Plant', 90], ['Diamond Storm', 95], ['Draco Meteor', 90], ['Muddy Water', 85], ['Sleep Powder', 75], ['Simple Beam', 100], ['Outrage', 100], ['Sheer Cold', 30], ['Beak Blast', 100], ['Trick-or-Treat', 100]]
    movesthatcanmiss2=[['Hydro Pump', 80], ['Steam Eruption', 95], ['X-Scissor', 100], ['Water Gun', 100], ['Nuzzle', 100], ['Hidden Power Fighting', 100], ['Snarl', 95], ['Venoshock', 100], ['Thousand Arrows', 100], ['Needle Arm', 100], ['Dragon Breath', 100], ['Cut', 95], ['Comet Punch', 85], ['Fake Tears', 100], ['Low Kick', 100], ['Bulldoze', 100], ['Psycho Shift', 100], ['Thrash', 100], ['Volt Switch', 100], ['Pound', 100], ['Silver Wind', 100], ['Precipice Blades', 85], ['Toxic Thread', 100], ['Hidden Power Psychic', 100], ['Hydro Cannon', 90], ['Air Slash', 95], ['Lava Plume', 100], ['Meteor Mash', 90], ['Icicle Crash', 90], ['Frustration', 100], ['Attack Order', 100], ['Entrainment', 100], ['Hold Back', 100], ["Nature's Madness", 90], ['Shadow Bone', 100], ['Ominous Wind', 100], ['Steel Beam', 95], ['Apple Acid', 100], ['Body Press', 100], ['Fishious Rend', 100], ['Bolt Beak', 100], ['Breaking Swipe', 100], ['Strange Steam', 95], ['Vise Grip', 100], ['Jaw Lock', 100], ['Pyro Ball', 90], ['Tar Shot', 100], ['Dynamax Cannon', 100], ['Snipe Shot', 100], ['Magic Powder', 100], ['Octolock', 100], ['Drum Beating', 100], ['Snap Trap', 100], ['Behemoth Blade', 100], ['Branch Poke', 100], ['Aura Wheel', 100], ['Overdrive', 100], ['Grav Apple', 100], ['Behemoth Bash', 100], ['Spirit Break', 100], ['Meteor Assault', 100], ['Eternabeam', 90], ['Dragon Darts', 100]]
    movesthatcanmiss=dict(movesthatcanmiss1+movesthatcanmiss2)
    #check if can miss
    if move in movesthatcanmiss.keys() and notimmune and targetnotprotected and targetmon and not semiinv:
        try: 
            acc_modifier=accuracy_modifier(attacker['accuracy'],target['evasion'])*results['Gravity']
            #compound eyes, victory star
            if attacker['pokemon'] in ['Venonat', 'Joltik', 'Yanma', 'Vivillon', 'Nincada', 'Dustox', 'Dottler', 'Galvantula', 'Butterfree-Gmax', 'Scatterbug', 'Butterfree', 'Blipbug']:
                acc_modifier=acc_modifier*1.3
            if attacker['pokemon'] in ['Victini']:
                acc_modifier=acc_modifier*1.1
            #no guard
            if attacker['pokemon'] in ['Machamp', 'Pidgeot-Mega', 'Golett', 'Lycanroc-Midnight', 'Machoke', 'Golurk', 'Honedge', 'Karrablast', 'Doublade', 'Machamp-Gmax', 'Machop']:
                acc_modifier=100000000
            #hustle cant be implemented right now
            #rain mod
            if move in ['Thunder','Hurricane'] and results['Rain']:
                acc_modifier=100000000
            if move in ['Blizzard'] and results['Hail']:
                acc_modifier=100000000
            results=luckappend(line,results,attacker,f"Mon Used a Move That Can Miss ({move})",100-min(movesthatcanmiss[move]*acc_modifier,100))
            results=luckappend(line,results,target,f"Target of Move That Can Miss ({move})",-(100-min(movesthatcanmiss[move]*acc_modifier,100)))
        except:
            pass
    #check for miss
    movehit=True
    if line[3].find("|[miss]")>-1 and notimmune and targetnotprotected and targetmon and not semiinv:
        results=miss_function(line,attacker,target,move,results)
        attacker['moves'][move]['hits']+=-1
        movehit=False
    #check if can crit
    movesthatcancrit=['Scratch', 'Anchor Shot', 'Avalanche', 'Sand Tomb', 'Fire Punch', 'Infestation', 'Superpower', 'Zing Zap', 'Giga Drain', 'Chatter', 'Ice Punch', 'Tail Slap', 'Double Slap', 'Thunder Shock', 'Splintered Stormshards', 'Sky Uppercut', 'Hyper Beam', 'Dynamic Punch', 'Poison Sting', 'Dig', 'Focus Blast', 'Liquidation', 'Double Kick', 'Ice Ball', 'Round', 'False Swipe', 'Crush Claw', 'Shadow Sneak', 'Tectonic Rage', 'Hidden Power Electric', 'Seed Bomb', 'Hidden Power Fire', 'Chip Away', 'Metal Claw', 'Acid', 'Vital Throw', 'Shock Wave', 'Baddy Bad', 'Accelerock', 'Aurora Beam', 'Heart Stamp', 'Magma Storm', 'Crunch', 'Aeroblast', 'Explosion', 'Gigavolt Havoc', 'Moongeist Beam', 'Revenge', 'Clear Smog', 'Wake-Up Slap', 'Pursuit', 'Head Smash', 'Earthquake', 'Incinerate', 'Water Pulse', 'Dragon Pulse', 'Glitzy Glow', 'Acid Spray', 'Thunder Punch', 'Extrasensory', 'Blizzard', 'Blast Burn', 'Paleo Wave', 'Mud-Slap', 'Inferno Overdrive', 'Freeze-Dry', 'Overheat', 'Savage Spin-Out', 'Flame Charge', 'Dizzy Punch', 'Flying Press', 'Lunge', 'Prismatic Laser', 'U-turn', 'Future Sight', 'Fire Lash', 'Smelling Salts', 'Burn Up', 'Catastropika', 'Bug Bite', 'Hidden Power Ghost', 'Shell Trap', 'Hyperspace Hole', 'Sky Drop', 'Crabhammer', 'Light That Burns the Sky', 'Darkest Lariat', 'Hidden Power', 'Razor Leaf', 'Head Charge', 'Dive', 'Signal Beam', 'Rock Tomb', 'Power Whip', 'Buzzy Buzz', "Let's Snuggle Forever", 'Psychic Fangs', 'Bind', 'Throat Chop', 'Parabolic Charge', 'Retaliate', 'Steamroller', 'Bullet Seed', 'Freezy Frost', 'Aqua Jet', 'Flame Burst', 'Thief', 'Astonish', 'Dream Eater', 'Energy Ball', 'Fury Swipes', 'Belch', 'Power Trip', 'Fury Cutter', 'Iron Tail', 'Hidden Power Flying', 'Egg Bomb', 'Payback', 'Fusion Flare', 'Boomburst', 'Secret Sword', 'Thunder Fang', 'Charge Beam', 'Rapid Spin', 'Skull Bash', 'Clamp', 'Rock Throw', 'Secret Power', 'Fairy Wind', 'Water Shuriken', 'Struggle Bug', 'Ice Fang', 'Self-Destruct', 'Sinister Arrow Raid', 'Stored Power', 'Tri Attack', 'Psychic', 'Electroweb', 'Weather Ball', 'Shattered Psyche', 'Whirlpool', 'Smog', 'Assurance', 'Icy Wind', 'Steel Wing', 'Core Enforcer', 'Synchronoise', 'Zippy Zap', 'Petal Dance', 'Iron Head', 'Trop Kick', 'Headbutt', 'Drain Punch', 'Bug Buzz', 'Fire Fang', 'Sludge', 'Mist Ball', 'Jump Kick', 'Water Spout', 'Ice Shard', 'Earth Power', 'Stomping Tantrum', 'Bolt Strike', 'Bite', 'Sappy Seed', 'Mega Kick', 'Inferno', 'Rock Climb', 'Rock Blast', 'Feint', 'Sucker Punch', 'Dragon Ascent', 'Freeze Shock', 'Peck', 'Drill Run', 'Leafage', 'Dark Pulse', 'Flash Cannon', 'Floaty Fall', 'Poison Fang', 'Dazzling Gleam', 'Double-Edge', 'Hidden Power Rock', 'Sludge Bomb', 'Lick', 'Fire Spin', 'Close Combat', 'Bone Rush', 'Slam', 'Aqua Tail', 'Strength', 'Fusion Bolt', 'Rage', 'Hidden Power Dark', 'Psycho Boost', 'Surf', 'Gear Grind', 'Shadow Ball', 'Eruption', 'Barrage', 'Shadow Force', 'Bonemerang', 'Cross Poison', 'Low Sweep', 'Sludge Wave', 'Leaf Tornado', 'Hyper Fang', 'Covet', 'Karate Chop', 'Fell Stinger', 'Thunder', 'Constrict', 'Razor Wind', 'Water Pledge', 'Brine', 'Hammer Arm', 'Last Resort', 'Pulverizing Pancake', 'Bullet Punch', 'Brick Break', 'Pay Day', 'Oblivion Wing', 'Origin Pulse', 'Stomp', 'Poison Tail', 'Bone Club', 'Fire Blast', 'Brave Bird', 'Gust', 'Mud Bomb', 'Leaf Blade', 'Sparkly Swirl', 'Twineedle', 'Solar Blade', 'Splishy Splash', 'Spirit Shackle', 'Continental Crush', 'Mystical Fire', 'Confusion', 'Pluck', 'Frost Breath', 'Roar of Time', 'Fury Attack', 'Swift', 'High Jump Kick', 'Brutal Swing', 'Petal Blizzard', 'Wing Attack', 'Hidden Power Steel', 'Wood Hammer', 'Hidden Power Water', 'Hyperspace Fury', 'Fiery Dance', 'Echoed Voice', 'Smack Down', "Land's Wrath", 'Mega Punch', 'Revelation Dance', 'Night Daze', 'Dragon Tail', 'Flare Blitz', 'Ice Hammer', 'V-create', 'Acid Downpour', 'Shadow Claw', 'Sacred Fire', 'Ice Beam', 'Facade', 'Vice Grip', 'Hidden Power Ice', 'Extreme Speed', 'Poison Jab', 'Take Down', 'Phantom Force', 'Double Iron Bash', 'Mind Blown', 'Multi-Attack', 'Zap Cannon', 'Magnet Bomb', 'Absorb', 'Waterfall', 'Judgment', 'Hidden Power Bug', 'Psybeam', 'Knock Off', 'Octazooka', 'Hyper Voice', 'Double Hit', 'Spark', 'Stone Edge', 'Rock Wrecker', 'Bouncy Bubble', 'Draining Kiss', 'Mud Shot', 'Mirror Shot', 'Megahorn', 'Acrobatics', 'Fleur Cannon', 'Dragon Rush', 'Solar Beam', 'Mach Punch', 'Luster Purge', 'Breakneck Blitz', 'Snore', 'Submission', 'Vacuum Wave', 'Thunderbolt', 'Circle Throw', 'All-Out Pummeling', 'Flame Wheel', 'Hidden Power Poison', 'Subzero Slammer', 'Fire Pledge', 'Bounce', 'Photon Geyser', 'Giga Impact', 'Dragon Claw', 'Soul-Stealing 7-Star Strike', 'Scald', 'Uproar', 'Force Palm', 'Hurricane', 'Ice Burn', 'Cross Chop', 'Psyshock', 'Hidden Power Grass', 'Techno Blast', 'Gunk Shot', 'Wild Charge', 'Dragon Hammer', 'Horn Attack', 'Blaze Kick', 'Psystrike', 'Spike Cannon', 'Horn Leech', 'Searing Shot', 'Supersonic Skystrike', 'Arm Thrust', 'Dual Chop', 'Foul Play', 'Twister', 'Focus Punch', 'Slash', 'Rollout', 'Icicle Spear', 'Wrap', 'Leech Life', 'Sacred Sword', 'Hex', 'Bubble', 'Quick Attack', 'Glaciate', 'Psycho Cut', 'Sizzly Slide', 'Rock Smash', 'Volt Tackle', 'Grass Pledge', 'Sparkling Aria', 'Vine Whip', 'Ember', 'Spacial Rend', 'Light of Ruin', 'Stoked Sparksurfer', 'Powder Snow', 'Power-Up Punch', 'Spectral Thief', 'Moonblast', 'Hydro Vortex', 'Thousand Waves', 'Rock Slide', 'Aura Sphere', 'Drill Peck', 'Storm Throw', 'Heat Wave', 'Tackle', 'Discharge', 'Razor Shell', 'Hidden Power Ground', 'Rolling Kick', 'Blue Flare', 'Sky Attack', 'Power Gem', 'Mega Drain', 'Genesis Supernova', 'High Horsepower', 'Black Hole Eclipse', 'Pollen Puff', 'Triple Kick', 'Night Slash', 'Plasma Fists', 'Pin Missile', 'First Impression', 'Fly', 'Relic Song', 'Fake Out', 'Ancient Power', 'Bubble Beam', 'Play Rough', 'Zen Headbutt', 'Clanging Scales', 'Shadow Strike', 'Hidden Power Dragon', 'Corkscrew Crash', 'Struggle', 'Body Slam', 'Seed Flare', 'Leaf Storm', 'Air Cutter', 'Flamethrower', 'Doom Desire', 'Sunsteel Strike', 'Twinkle Tackle', 'Frenzy Plant', 'Diamond Storm', 'Never-Ending Nightmare', 'Draco Meteor', 'Muddy Water', 'Outrage', 'Malicious Moonsault', 'Beak Blast', 'Hydro Pump', 'Steam Eruption', 'Smart Strike', 'X-Scissor', 'Disarming Voice', 'Water Gun', 'Clangorous Soulblaze', "Magikarp's Revenge", 'Nuzzle', 'Hidden Power Fighting', 'Snarl', 'Venoshock', 'Thousand Arrows', 'Needle Arm', 'Dragon Breath', 'Searing Sunraze Smash', 'Cut', 'Comet Punch', 'Aerial Ace', 'Bulldoze', 'Menacing Moonraze Maelstrom', 'Thrash', 'Volt Switch', 'Pound', 'Silver Wind', 'Precipice Blades', 'Bloom Doom', 'Hidden Power Psychic', 'Hydro Cannon', 'Air Slash', 'Magical Leaf', '10,000,000 Volt Thunderbolt', 'Lava Plume', 'Meteor Mash', 'Shadow Punch', 'Feint Attack', 'Icicle Crash', 'Devastating Drake', 'Oceanic Operetta', 'Attack Order', 'Hold Back', 'Shadow Bone', 'Ominous Wind', 'Steel Beam', 'Apple Acid', 'Body Press', 'Fishious Rend', 'Bolt Beak', 'Breaking Swipe', 'Strange Steam', 'Vise Grip', 'Jaw Lock', 'Pyro Ball', 'Dynamax Cannon', 'Snipe Shot', 'Drum Beating', 'Snap Trap', 'Behemoth Blade', 'Branch Poke', 'Aura Wheel', 'Overdrive', 'Grav Apple', 'Behemoth Bash', 'Spirit Break', 'False Surrender', 'Meteor Assault', 'Eternabeam', 'Dragon Darts']
    increasedcrit=['Aeroblast','Air Cutter','Attack Order','Blaze Kick','Crabhammer','Cross Chop','Cross Poison','Drill Run','Karate Chop','Leaf Blade','Night Slash','Poison Tail','Psycho Cut','Razor Leaf','Razor Wind','Shadow Claw','Sky Attack','Slash','Snipe Shot','Spacial Rend','Stone Edge']
    movesthatalwayscrit=['Frost Breath','Storm Throw','Zippy Zap']
    #check for merciless
    notmerciless=True
    if attacker['pokemon'] in ['Mareanie','Toxapex'] and (target['psn']!=None or target['tox']!=None):
        notmerciless=False
    if move in movesthatalwayscrit and notimmune and targetnotprotected and targetmon and movehit and target['pokemon'] not in ['Type:Null','Slowbro-Mega','Turtonator']:
        results=luckappend(line,results,attacker,f"Mon Used Move That Always Crits ({move})",-100)
        results=luckappend(line,results,target,f"Target of Move That Always Crits ({move})",100)
    elif move in increasedcrit and notimmune and targetnotprotected and targetmon and movehit and notmerciless and target['pokemon'] not in ['Type:Null','Slowbro-Mega','Turtonator']:
        try:
            if attacker['Focus Energy']:
                results=luckappend(line,results,attacker,f"Mon With Focus Energy Used Move With Increased Crit Chance ({move})",-100)
                results=luckappend(line,results,target,f"Target of Mon With Focus Energy Using Move With Increased Crit Chance ({move})",100)
            elif attacker['pokemon'] in ['Unfezant', 'Pidove', 'Honchkrow', 'Tranquill', 'Togepi', 'Murkrow', 'Absol']:
                results=luckappend(line,results,attacker,f"Super Luck Mon Used Move With Increased Crit Chance ({move})",-50)
                results=luckappend(line,results,target,f"Target of Super Luck Mon Using Move With Increased Crit Chance ({move})",50)
            else:
                results=luckappend(line,results,attacker,f"Mon Used Move With Increased Crit Chance ({move})",-12.5)
                results=luckappend(line,results,target,f"Target of Move With Increased Crit Chance ({move})",12.5)
        except Exception as e:
            print(move)
    elif move in movesthatcancrit and notimmune and targetnotprotected and targetmon and movehit and notmerciless and target['pokemon'] not in ['Type:Null','Slowbro-Mega','Turtonator']:
        try:
            if attacker['Focus Energy']:
                results=luckappend(line,results,attacker,f"Mon With Focus Energy Used Move With Crit Chance ({move})",-50)
                results=luckappend(line,results,target,f"Target of Mon With Focus Energy Using Move With Crit Chance ({move})",50)
            elif attacker['pokemon'] in ['Unfezant', 'Pidove', 'Honchkrow', 'Tranquill', 'Togepi', 'Murkrow', 'Absol']:
                results=luckappend(line,results,attacker,f"Super Luck Mon Used Move With Crit Chance ({move})",-12.5)
                results=luckappend(line,results,target,f"Target of Super Luck Mon Using Move With Crit Chance ({move})",12.5)
            else:
                results=luckappend(line,results,attacker,f"Mon Used Move With Crit Chance ({move})",-4.167)
                results=luckappend(line,results,target,f"Target of Move With Crit Chance ({move})",4.167)
        except:
            pass
    #moves with secondary effect
    #check if already statused
    statusdict=dict([['Thunder Punch', 'par'], ['Fire Punch', 'brn'], ['Fire Fang', 'brn'], ['Pyro Ball', 'brn'], ['Ice Punch', 'frz'], ['Ice Fang', 'frz'], ['Thunder Fang', 'par'], ['Thunder Shock', 'par'], ['Poison Sting', 'psn'], ['Blizzard', 'frz'], ['Freeze-Dry', 'frz'], ['Relic Song', 'slp'], ['Sludge', 'psn'], ['Secret Power', 'par'], ['Smog', 'psn'], ['Body Slam', 'par'], ['Bolt Strike', 'par'], ['Flamethrower', 'brn'], ['Freeze Shock', 'par'], ['Poison Fang', 'tox'], ['Sludge Bomb', 'psn'], ['Lick', 'par'], ['Cross Poison', 'psn'], ['Sludge Wave', 'psn'], ['Thunder', 'par'], ['Poison Tail', 'psn'], ['Fire Blast', 'brn'], ['Twineedle', 'psn'], ['Splishy Splash', 'par'], ['Steam Eruption', 'brn'], ['Flare Blitz', 'brn'], ['Sacred Fire', 'brn'], ['Ice Beam', 'frz'], ['Poison Jab', 'psn'], ['Spark', 'par'], ['Dragon Breath', 'par'], ['Thunderbolt', 'par'], ['Flame Wheel', 'brn'], ['Bounce', 'par'], ['Scald', 'brn'], ['Force Palm', 'par'], ['Ice Burn', 'brn'], ['Gunk Shot', 'psn'], ['Blaze Kick', 'brn'], ['Lava Plume', 'brn'], ['Searing Shot', 'brn'], ['Volt Tackle', 'par'], ['Ember', 'brn'], ['Powder Snow', 'frz'], ['Heat Wave', 'brn'], ['Discharge', 'par'], ['Blue Flare', 'brn']])
    immunebytype={
        'par':['Yamper', 'Pichu', 'Electivire', 'Galvantula', 'Magnemite', 'Boltund', 'Golem-Alola', 'Stunfisk', 'Flaaffy', 'Plusle', 'Thundurus', 'Eelektrik', 'Ampharos', 'Manectric-Mega', 'Luxray', 'Magnezone', 'Manectric', 'Ampharos-Mega', 'Voltorb', 'Rotom-Frost', 'Electabuzz', 'Minun', 'Shinx', 'Zebstrika', 'Rotom', 'Tynamo', 'Electrike', 'Toxel', 'Toxtricity', 'Joltik', 'Zeraora', 'Magneton', 'Blitzle', 'Electrode', 'Elekid', 'Graveler-Alola', 'Charjabug', 'Zapdos', 'Rotom-Mow', 'Luxio', 'Zekrom', 'Xurkitree', 'Geodude-Alola', 'Raikou', 'Pincurchin', 'Morpeko', 'Dracozolt', 'Arctozolt', 'Chinchou', 'Mareep', 'Togedemaru', 'Pikachu-Gmax', 'Toxtricity-Gmax', 'Rotom-Wash', 'Thundurus-Therian', 'Pachirisu', 'Heliolisk', 'Rotom-Heat', 'Jolteon', 'Rotom-Fan', 'Vikavolt', 'Raichu-Alola', 'Lanturn', 'Pikachu', 'Emolga', 'Tapu Koko', 'Dedenne', 'Helioptile', 'Raichu', 'Eelektross'],
        'brn':['Scorbunny', 'Raboot', 'Cinderace', 'Quilava', 'Tepig', 'Charmander', 'Salandit', 'Darumaka', 'Combusken', 'Delphox', 'Talonflame', 'Moltres', 'Turtonator', 'Carkol', 'Coalossal', 'Pansear', 'Simisear', 'Infernape', 'Heatran', 'Monferno', 'Reshiram', 'Litten', 'Braixen', 'Pyroar', 'Chandelure', 'Litwick', 'Rapidash', 'Blacephalon', 'Arcanine', 'Volcarona', 'Fletchinder', 'Lampent', 'Charizard-Mega-X', 'Oricorio', 'Ninetales', 'Ho-Oh', 'Slugma', 'Growlithe', 'Litleo', 'Torkoal', 'Flareon', 'Darmanitan', 'Ponyta', 'Houndour', 'Sizzlipede', 'Centiskorch', 'Charmeleon', 'Camerupt', 'Victini', 'Heatmor', 'Magmortar', 'Numel', 'Houndoom-Mega', 'Emboar', 'Houndoom', 'Marowak-Alola', 'Magcargo', 'Blaziken', 'Incineroar', 'Chimchar', 'Volcanion', 'Coalossal-Gmax', 'Centiskorch-Gmax', 'Charizard-Gmax', 'Magby', 'Charizard', 'Fennekin', 'Cyndaquil', 'Magmar', 'Groudon-Primal', 'Pignite', 'Blaziken-Mega', 'Rotom-Heat', 'Entei', 'Charizard-Mega-Y', 'Vulpix', 'Torracat', 'Larvesta', 'Torchic', 'Salazzle', 'Typhlosion', 'Camerupt-Mega'],
        'psn':['Weezing-Galar', 'Salandit', 'Venusaur-Mega', 'Weezing', 'Qwilfish', 'Roselia', 'Gastly', 'Beedrill-Mega', 'Grimer', 'Seviper', 'Scolipede', 'Zubat', 'Toxicroak', 'Tentacruel', 'Foongus', 'Weepinbell', 'Stunky', 'Venusaur', 'Muk-Alola', 'Croagunk', 'Gloom', 'Koffing', 'Bellsprout', 'Mareanie', 'Swalot', 'Nidoran-F', 'Nidoran-M', 'Skrelp', 'Crobat', 'Venipede', 'Amoonguss', 'Gengar-Mega', 'Nidoking', 'Toxel', 'Toxtricity', 'Vileplume', 'Drapion', 'Haunter', 'Weedle', 'Skorupi', 'Muk', 'Skuntank', 'Grimer-Alola', 'Garbodor', 'Toxapex', 'Ivysaur', 'Nihilego', 'Gulpin', 'Trubbish', 'Golbat', 'Whirlipede', 'Eternatus', 'Beedrill', 'Spinarak', 'Budew', 'Nidoqueen', 'Naganadel', 'Gengar', 'Toxtricity-Gmax', 'Garbodor-Gmax', 'Gengar-Gmax', 'Oddish', 'Bulbasaur', 'Dustox', 'Arbok', 'Venonat', 'Dragalge', 'Roserade', 'Venomoth', 'Nidorino', 'Nidorina', 'Poipole', 'Tentacool', 'Victreebel', 'Salazzle', 'Ariados', 'Ekans', 'Kakuna'],
        'tox':['Weezing-Galar', 'Salandit', 'Venusaur-Mega', 'Weezing', 'Qwilfish', 'Roselia', 'Gastly', 'Beedrill-Mega', 'Grimer', 'Seviper', 'Scolipede', 'Zubat', 'Toxicroak', 'Tentacruel', 'Foongus', 'Weepinbell', 'Stunky', 'Venusaur', 'Muk-Alola', 'Croagunk', 'Gloom', 'Koffing', 'Bellsprout', 'Mareanie', 'Swalot', 'Nidoran-F', 'Nidoran-M', 'Skrelp', 'Crobat', 'Venipede', 'Amoonguss', 'Gengar-Mega', 'Nidoking', 'Toxel', 'Toxtricity', 'Vileplume', 'Drapion', 'Haunter', 'Weedle', 'Skorupi', 'Muk', 'Skuntank', 'Grimer-Alola', 'Garbodor', 'Toxapex', 'Ivysaur', 'Nihilego', 'Gulpin', 'Trubbish', 'Golbat', 'Whirlipede', 'Eternatus', 'Beedrill', 'Spinarak', 'Budew', 'Nidoqueen', 'Naganadel', 'Gengar', 'Toxtricity-Gmax', 'Garbodor-Gmax', 'Gengar-Gmax', 'Oddish', 'Bulbasaur', 'Dustox', 'Arbok', 'Venonat', 'Dragalge', 'Roserade', 'Venomoth', 'Nidorino', 'Nidorina', 'Poipole', 'Tentacool', 'Victreebel', 'Salazzle', 'Ariados', 'Ekans', 'Kakuna'],
        'frz':['Mr.Mime-Galar', 'Darumaka-Galar', 'Darmanitan-Galar', 'Vanillish', 'Jynx', 'Swinub', 'Crabominable', 'Kyurem-White', 'Kyurem', 'Sneasel', 'Glalie', 'Glaceon', 'Sandslash-Alola', 'Rotom-Frost', 'Abomasnow', 'Abomasnow-Mega', 'Spheal', 'Ninetales-Alola', 'Sealeo', 'Snorunt', 'Vanilluxe', 'Cubchoo', 'Dewgong', 'Sandshrew-Alola', 'Cloyster', 'Mr.Rime', 'Snom', 'Frosmoth', 'Eiscue', 'Arctozolt', 'Arctovish', 'Glalie-Mega', 'Vanillite', 'Piloswine', 'Lapras-Gmax', 'Snover', 'Aurorus', 'Walrein', 'Smoochum', 'Amaura', 'Avalugg', 'Weavile', 'Cryogonal', 'Delibird', 'Articuno', 'Vulpix-Alola', 'Mamoswine', 'Beartic', 'Bergmite', 'Kyurem-Black', 'Froslass', 'Lapras', 'Regice'],
        'slp':[],
    }
    notimmunebytype=True
    notstatused=True
    if move in statusdict.keys() and (target['psn']!=None or target['tox']!=None or target['par']!=None or target['frz']!=None or target['brn']!=None or target['slp']!=None):
        notstatused=False
    if move in statusdict.keys():
        status=statusdict[move]
        if target['pokemon'] in immunebytype[status] and (attacker['pokemon'] not in ['Salazzle','Salandit'] or status not in ['psn','tox']):
            notimmunebytype=False
    if movedfirst: 
        moveswithsecondaryeffect=dict([['Fire Punch', 10],['Fire Fang', 19],['Ice Fang', 19],['Thunder Fang', 19], ['Zing Zap', 30], ['Ice Punch', 10], ['Thunder Shock', 10], ['Poison Sting', 30], ['Focus Blast', 10], ['Liquidation', 20], ['Crush Claw', 50], ['Metal Claw', 10], ['Acid', 10], ['Aurora Beam', 10], ['Heart Stamp', 30], ['Crunch', 20], ['Water Pulse', 20], ['Thunder Punch', 10], ['Extrasensory', 10], ['Blizzard', 10], ['Paleo Wave', 20], ['Freeze-Dry', 10], ['Dizzy Punch', 20], ['Signal Beam', 10], ['Steamroller', 30], ['Astonish', 30], ['Energy Ball', 10], ['Iron Tail', 30], ['Charge Beam', 70], ['Secret Power', 30], ['Tri Attack', 20], ['Psychic', 10], ['Smog', 40], ['Steel Wing', 10], ['Iron Head', 30], ['Headbutt', 30], ['Bug Buzz', 10], ['Sludge', 30], ['Mist Ball', 50], ['Earth Power', 10], ['Bolt Strike', 20], ['Bite', 30], ['Rock Climb', 20], ['Freeze Shock', 30], ['Dark Pulse', 20], ['Flash Cannon', 10], ['Floaty Fall', 30], ['Poison Fang', 50], ['Sludge Bomb', 30], ['Lick', 30], ['Shadow Ball', 20], ['Cross Poison', 10], ['Sludge Wave', 10], ['Leaf Tornado', 50], ['Hyper Fang', 10], ['Thunder', 30], ['Constrict', 10], ['Stomp', 30], ['Poison Tail', 10], ['Bone Club', 10], ['Fire Blast', 10], ['Mud Bomb', 30], ['Twineedle', 20], ['Splishy Splash', 30], ['Confusion', 10], ['Fiery Dance', 50], ['Night Daze', 40], ['Flare Blitz', 10], ['Sacred Fire', 50], ['Ice Beam', 10], ['Poison Jab', 30], ['Double Iron Bash', 51], ['Waterfall', 20], ['Psybeam', 10], ['Octazooka', 50], ['Spark', 30], ['Mirror Shot', 30], ['Dragon Rush', 20], ['Luster Purge', 50], ['Snore', 30], ['Thunderbolt', 10], ['Flame Wheel', 10], ['Bounce', 30], ['Scald', 30], ['Force Palm', 30], ['Hurricane', 30], ['Ice Burn', 30], ['Gunk Shot', 30], ['Blaze Kick', 10], ['Searing Shot', 30], ['Twister', 20], ['Bubble', 10], ['Rock Smash', 50], ['Volt Tackle', 10], ['Ember', 10], ['Powder Snow', 10], ['Moonblast', 30], ['Rock Slide', 30], ['Heat Wave', 10], ['Discharge', 30], ['Razor Shell', 50], ['Rolling Kick', 30], ['Blue Flare', 20], ['Sky Attack', 30], ['Relic Song', 10], ['Ancient Power', 10], ['Bubble Beam', 10], ['Play Rough', 10], ['Zen Headbutt', 20], ['Shadow Strike', 50], ['Body Slam', 30], ['Seed Flare', 40], ['Flamethrower', 10], ['Diamond Storm', 50], ['Muddy Water', 30], ['Steam Eruption', 30], ['Needle Arm', 30], ['Dragon Breath', 30], ['Silver Wind', 10], ['Air Slash', 30], ['Lava Plume', 30], ['Meteor Mash', 20], ['Icicle Crash', 30], ['Shadow Bone', 20], ['Ominous Wind', 10], ['Strange Steam', 20], ['Pyro Ball', 10]])
    else:    
        moveswithsecondaryeffect=dict([['Fire Punch', 10],['Fire Fang', 10],['Ice Fang', 10],['Thunder Fang', 10], ['Zing Zap', 30], ['Ice Punch', 10], ['Thunder Shock', 10], ['Poison Sting', 30], ['Focus Blast', 10], ['Liquidation', 20], ['Crush Claw', 50], ['Metal Claw', 10], ['Acid', 10], ['Aurora Beam', 10], ['Heart Stamp', 30], ['Crunch', 20], ['Water Pulse', 20], ['Thunder Punch', 10], ['Extrasensory', 10], ['Blizzard', 10], ['Paleo Wave', 20], ['Freeze-Dry', 10], ['Dizzy Punch', 20], ['Signal Beam', 10], ['Steamroller', 30], ['Astonish', 30], ['Energy Ball', 10], ['Iron Tail', 30], ['Charge Beam', 70], ['Secret Power', 30], ['Tri Attack', 20], ['Psychic', 10], ['Smog', 40], ['Steel Wing', 10], ['Iron Head', 30], ['Headbutt', 30], ['Bug Buzz', 10], ['Sludge', 30], ['Mist Ball', 50], ['Earth Power', 10], ['Bolt Strike', 20], ['Bite', 30], ['Rock Climb', 20], ['Freeze Shock', 30], ['Dark Pulse', 20], ['Flash Cannon', 10], ['Floaty Fall', 30], ['Poison Fang', 50], ['Sludge Bomb', 30], ['Lick', 30], ['Shadow Ball', 20], ['Cross Poison', 10], ['Sludge Wave', 10], ['Leaf Tornado', 50], ['Hyper Fang', 10], ['Thunder', 30], ['Constrict', 10], ['Stomp', 30], ['Poison Tail', 10], ['Bone Club', 10], ['Fire Blast', 10], ['Mud Bomb', 30], ['Twineedle', 20], ['Splishy Splash', 30], ['Confusion', 10], ['Fiery Dance', 50], ['Night Daze', 40], ['Flare Blitz', 10], ['Sacred Fire', 50], ['Ice Beam', 10], ['Poison Jab', 30], ['Double Iron Bash', 51], ['Waterfall', 20], ['Psybeam', 10], ['Octazooka', 50], ['Spark', 30], ['Mirror Shot', 30], ['Dragon Rush', 20], ['Luster Purge', 50], ['Snore', 30], ['Thunderbolt', 10], ['Flame Wheel', 10], ['Bounce', 30], ['Scald', 30], ['Force Palm', 30], ['Hurricane', 30], ['Ice Burn', 30], ['Gunk Shot', 30], ['Blaze Kick', 10], ['Searing Shot', 30], ['Twister', 20], ['Bubble', 10], ['Rock Smash', 50], ['Volt Tackle', 10], ['Ember', 10], ['Powder Snow', 10], ['Moonblast', 30], ['Rock Slide', 30], ['Heat Wave', 10], ['Discharge', 30], ['Razor Shell', 50], ['Rolling Kick', 30], ['Blue Flare', 20], ['Sky Attack', 30], ['Relic Song', 10], ['Ancient Power', 10], ['Bubble Beam', 10], ['Play Rough', 10], ['Zen Headbutt', 20], ['Shadow Strike', 50], ['Body Slam', 30], ['Seed Flare', 40], ['Flamethrower', 10], ['Diamond Storm', 50], ['Muddy Water', 30], ['Steam Eruption', 30], ['Needle Arm', 30], ['Dragon Breath', 30], ['Silver Wind', 10], ['Air Slash', 30], ['Lava Plume', 30], ['Meteor Mash', 20], ['Icicle Crash', 30], ['Shadow Bone', 20], ['Ominous Wind', 10], ['Strange Steam', 20], ['Pyro Ball', 10]])
    flinchmoves=['Zing Zap', 'Heart Stamp', 'Extrasensory', 'Steamroller', 'Astonish', 'Iron Head', 'Headbutt', 'Bite', 'Dark Pulse', 'Floaty Fall', 'Hyper Fang', 'Stomp', 'Bone Club', 'Waterfall', 'Double Iron Bash', 'Dragon Rush', 'Snore', 'Twister', 'Rock Slide', 'Rolling Kick', 'Sky Attack', 'Fake Out', 'Zen Headbutt', 'Needle Arm', 'Air Slash', 'Icicle Crash']
    selfboostmoves=['Metal Claw', 'Flame Charge', 'Charge Beam', 'Steel Wing', 'Fiery Dance', 'Power-Up Punch', 'Ancient Power', 'Diamond Storm', 'Silver Wind', 'Meteor Mash', 'Ominous Wind']
    if move in moveswithsecondaryeffect.keys() and notimmune and notstatused and targetnotprotected and targetmon and notimmunebytype and movehit and (targetalive or move in selfboostmoves) and (movedfirst or move not in flinchmoves):
        secondaryeffectmodifier=1
        if attacker['pokemon'] in ['Chansey','Blissey','Dunsparce','Togepi','Togetic','Togekiss','Shaymin-Sky','Jirachi','Happiny','Deerling','Sawsbuck','Meloetta']:
            secondaryeffectmodifier=2
        try:
            results=luckappend(line,results,attacker,f"Mon Used Move With Secondary Effect Chance ({move})",-moveswithsecondaryeffect[move]*secondaryeffectmodifier)
            results=luckappend(line,results,target,f"Target of Move With Secondary Effect Chance ({move})",moveswithsecondaryeffect[move]*secondaryeffectmodifier)
            #check for secondary effect
            results=secondary_check(attacker,target,move,line,results,parsedlogfile,attackingteam)
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
        if line[3].find("[notarget]")>-1:
            miss=True
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
        if results['team1']['G-Max Steelsurge']!=None:results['team2']['G-Max Steelsurge']=attacker['nickname']
        if results['team2']['G-Max Steelsurge']!=None:results['team1']['G-Max Steelsurge']=attacker['nickname'] 
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
            'confusion':None,'psn':None,'brn':None,'par':None,'frz':None,'tox':None,'slp':None,'Curse':None,'atk':0,'def':0,'spa':0,'spd':0,'spe':0,'accuracy':0,'evasion':0,'Focus Energy':False,'semiinv':False,'moves':{}
        })  
    elif line[3].split("|",1)[0]=="p2":
        results['team2']['roster'].append({
            'pokemon':line[3].split("|")[1], 'startform':adjustedmon,'nickname':adjustedmon,
            'kills':0,'deaths':0,'causeofdeath':None,'support':0,'damagedone':0,'hphealed':0,'luck':0,'remaininghealth':100,'lines':[],
            'confusion':None,'psn':None,'brn':None,'par':None,'frz':None,'tox':None,'slp':None,'Curse':None,'atk':0,'def':0,'spa':0,'spd':0,'spe':0,'accuracy':0,'evasion':0,'Focus Energy':False,'semiinv':False,'moves':{}
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
        activemon=line[3].split("|")[3].split(": ")[1]
        mon[status]=activemon
        activemon=roster_search(otherteam,activemon,results)
        results=luckappend(line,results,mon,f"Mon Was Statused Due to Ability",-70)
        results=luckappend(line,results,activemon,f"Opponent Was Statused Due to Ability",70)
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
    elif line[3].find("[from] move: Rest")>-1 or line[3].find("|slp")>-1: 
        turndata=list(filter(lambda x: x[1] == line[1] and x[0] > line[0], parsedlogfile))
        for line_ in turndata:
            if line_[2]=="heal" and line_[3].find(mon['nickname'])>-1:
                mon['slp']=mon['nickname']
                mon['tox']=None; mon['psn']=None; mon['brn']=None; mon['frz']=None; mon['par']=None
    else:
        movesthatcausestatus=dict([
            ['tox',['Toxic','Fling','Psycho Shift']],
            ['psn',['Toxic Thread','Poison Powder','Poison Gas','Baneful Bunker','Fling','Psycho Shift','G-Max Stun Shock']],
            ['brn',['Beak Blast','Will-O-Wisp','Fling','Psycho Shift']],
            ['par',['Thunder Wave','Nuzzle','Glare','Stoked Sparksurfer','Stun Spore','Zap Cannon','Fling','Psycho Shift','G-Max Stun Shock']],
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
            elif line_[2]=="activate" and line_[3].find(f"|ability: Synchronize")>-1 and mon[status]==None:
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
            movesthatconfuse=['Dynamic Punch','Confuse Ray','Chatter','Supersonic','Teeter Dance']
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
                setter['hphealed']+=healthremaining-priorhealth
                break
    if line[3].find("Focus Energy")>-1:
        mon=line[3].split("|")[0].split(": ")[1]
        team=line[3].split(": ")[0]
        mon=roster_search(team,mon,results)
        mon['Focus Energy']=True
    return line,parsedlogfile,results

def switch_drag_function(line,parsedlogfile,results):
    if line[3].split(":",1)[0]=="p1a":
        for mon in results['team1']['roster']:
            mon['atk']=0;mon['def']=0;mon['spa']=0;mon['spd']=0;mon['spe']=0;mon['accuracy']=0;mon['evasion']=0;mon['Focus Energy']=False
        results,line=namecheck(results,line,1)
    elif line[3].split(":",1)[0]=="p2a":
        for mon in results['team2']['roster']:
            mon['atk']=0;mon['def']=0;mon['spa']=0;mon['spd']=0;mon['spe']=0;mon['accuracy']=0;mon['evasion']=0;mon['Focus Energy']=False
        results,line=namecheck(results,line,2)
    return line,parsedlogfile,results

def alternate_switch_drag_function(line,parsedlogfile,results):
    if line[3].split(":",1)[0]=="p1a":
        for mon in results['team1']['roster']:
            mon['atk']=0;mon['def']=0;mon['spa']=0;mon['spd']=0;mon['spe']=0;mon['accuracy']=0;mon['evasion']=0;mon['Focus Energy']=False
            if mon['pokemon'] in ['Chansey','Blissey','Starmie','Celebi','Roselia','Swablu','Altaria','Budew','Happiny','Shaymin']:
                results,mon=reset_status(results,mon)
        results,line=namecheck(results,line,1)
    elif line[3].split(":",1)[0]=="p2a":
        for mon in results['team2']['roster']:
            mon['atk']=0;mon['def']=0;mon['spa']=0;mon['spd']=0;mon['spe']=0;mon['accuracy']=0;mon['evasion']=0;mon['Focus Energy']=False
            if mon['pokemon'] in ['Chansey','Blissey','Starmie','Celebi','Roselia','Swablu','Altaria','Budew','Happiny','Shaymin']:
                results,mon=reset_status(results,mon)
        results,line=namecheck(results,line,2)
    return line,parsedlogfile,results

def reset_status(results,mon):
    mon['tox']=None
    mon['psn']=None
    mon['brn']=None
    mon['par']=None
    mon['slp']=None
    mon['frz']=None
    return results,mon

def unboost_function(line,parsedlogfile,results):
    team=line[3].split(":")[0]
    mon=line[3].split(": ")[1].split("|")[0]
    stat=line[3].split("|")[1]
    boostnum=int(line[3].split("|")[2])
    mon=roster_search(team,mon,results)
    mon[stat]+=-boostnum
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
    elif line[3].find("Sandstorm")>-1 and line[3].find("upkeep")==-1:
        setterline=parsedlogfile[line[0]-1]
        thisteam=setterline[3].split(": ")[0]
        setter=setterline[3].split("|")[0].split(": ",1)[1]
        if thisteam=="p1a":
            results['team2']['Sandstorm']=setter
        elif thisteam=="p2a":
            results['team1']['Sandstorm']=setter
    elif line[3].find("Hail")>-1 and line[3].find("upkeep")==-1:
        setterline=parsedlogfile[line[0]-1]
        thisteam=setterline[3].split(": ")[0]
        setter=setterline[3].split("|")[0].split(": ",1)[1]
        if thisteam=="p1a":
            results['team2']['Hail']=setter
        elif thisteam=="p2a":
            results['team1']['Hail']=setter
    if line[3].find("Rain")>-1 or line[3].find("Drizzle")>-1 or line[3].find("Max Geyser")>-1:
        results['Rain']=True
    if line[3].find("Hail")>-1 or line[3].find("Snow Warning")>-1 or line[3].find("Max Hailstorm")>-1:
        results['Hail']=True
    elif line[3]=="none":
        results['team1']['Sandstorm']=None
        results['team1']['Hail']=None
        results['team2']['Sandstorm']=None
        results['team2']['Hail']=None
        results['Rain']=False
        results['Hail']=False
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
    results['team1']['G-Max Steelsurge']=None
    results['team2']['G-Max Steelsurge']=None
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
    results['Gravity']=1.0
    results['Rain']=False
    results['Hail']=False
    results['numberofturns']=0
    results['turns']=[]
    results['replay']=""
    results['significantevents']=[]
    results['luckcatalog']=[]
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
    #initialize output json
    #iterate through logfile
    try:
        results,parsedlogfile=prepare_parsedlogfile(logfile,replay)
        switchdraglines=list(filter(lambda x: x[2] in ["switch","drag"], parsedlogfile))[::-1]
        for line in switchdraglines:
            team=line[3].split(": ",)[0]
            nickname=line[3].split("|")[0].split(": ",)[1]
            pokemon=line[3].split("|")[1].split("-")[0]
            if pokemon.find(nickname)==-1:
                matchdata=list(filter(lambda x: x[0]>=line[0], parsedlogfile))
                for line_ in matchdata:
                    line_[3]=line_[3].replace(nickname,pokemon)
        for line in parsedlogfile:
            line,parsedlogfile,results=alternate_replay_parse_switch(line,parsedlogfile,results)
    except:
        results,parsedlogfile=prepare_parsedlogfile(logfile,replay)
        switchdraglines=list(filter(lambda x: x[2] in ["switch","drag"], parsedlogfile))[::-1]
        for line in switchdraglines:
            team=line[3].split(": ",)[0]
            nickname=line[3].split("|")[0].split(": ",)[1]
            pokemon=line[3].split("|")[1].split("-")[0]
            if pokemon.find(nickname)==-1:
                matchdata=list(filter(lambda x: x[0]>=line[0], parsedlogfile))
                for line_ in matchdata:
                    line_[3]=line_[3].replace(nickname,pokemon)
        for line in parsedlogfile:
            line,parsedlogfile,results=replay_parse_switch(line,parsedlogfile,results)
    #sort significant events
    results['significantevents']=sorted( results['significantevents'],key=lambda tup: tup[0])
    #sort luckcatalog
    results['luckcatalog']=sorted( results['luckcatalog'],key=lambda tup: tup[1])
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

def accuracy_modifier(accuracy,evasion):
    accuracy=accuracy_chart(accuracy)
    evasion=accuracy_chart(evasion)
    return accuracy/evasion

def accuracy_chart(boost):
    if boost==-6:
        return .333
    elif boost==-5:
        return .375
    elif boost==-4:
        return .429
    elif boost==-3:
        return .50
    elif boost==-2:
        return .60
    elif boost==-1:
        return .75
    elif boost==0:
        return 1
    elif boost==1:
        return 1.333
    elif boost==2:
        return 1.667
    elif boost==3:
        return 2
    elif boost==4:
        return 2.333
    elif boost==5:
        return 2.667
    elif boost==6:
        return 3