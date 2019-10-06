import requests
import json

from .luckfunctions import *

def replay_parse_switch(argument,parsedlogfile,results):
    switcher = {
        'damage': damage_function,
        'detailschange': detailschange_function,
        'drag': switch_drag_function,
        'heal':heal_function,
        'message': message_function,
        'move': move_function,
        'player': player_function,
        'poke': poke_function,
        'switch': switch_drag_function,
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
    logfile = requests.get(replay+".log").text.splitlines()
    parsedlogfile=[]
    line_number=0
    turn_number=0
    #initialize output json
    results=initializeoutput()
    results['replay']=replay
    #iterate through logfile
    for line in logfile:
        #remove unneeded lines
        line=line.replace(", M","").replace(", F","").replace("-*","").replace(", shiny","")
        linestoremove=["|","|teampreview","|start","|clearpoke","|upkeep"]
        linepurposestoremove=["j","c","l","teamsize","gen","gametype","tier","rule","-mega","seed","teampreview"]
        linepurpose=line.split("|",2)[1].replace("-","")
        #iterate turn number
        if linepurpose=="turn":
            turn_number+=1
            results['numberofturns']=turn_number
        #add turn data
        elif line not in linestoremove and linepurpose not in linepurposestoremove:
            lineremainder=line.split("|",2)[2]
            parsedlogfile.append([line_number,turn_number,linepurpose,lineremainder])
            line_number+=1
    #iterate through parsed logfile
    for line in parsedlogfile:
        line,parsedlogfile,results=replay_parse_switch(line,parsedlogfile,results)
    #sort significant events
    results['significantevents']=sorted( results['significantevents'],key=lambda tup: tup[0])
    #output results to json file
    with open('replayanalysis/NewParser/results.json', 'w') as f:
        json.dump(results,f,indent=2)
    return results

def damage_function(line,parsedlogfile,results):
    team=line[3].split(":",1)[0]
    pokemon=line[3].split(" ",1)[1].split("|")[0]
    healthremaining=int(line[3].split("|",1)[1].split(" ",1)[0].split("/",1)[0])
    #searchroster
    pokemon=roster_search(team,pokemon,results)
    #update remaining health
    previoushealth=pokemon['remaininghealth']
    pokemon['remaininghealth']=healthremaining
    damagedone=previoushealth-healthremaining
    #determine damager
    if line[3].find("[from]")>-1:
        #not direct damage consider future sight
        cause=None
    else:
        #search for damager
        damager,move=damager_search(parsedlogfile,line,team,pokemon,results,damagedone)
    #update fainted
    if healthremaining==0:
        pokemon['deaths']=1
        if damager: 
            damager['kills']+=1
            results['significantevents'].append([line[1],f"{damager['pokemon']} killed {pokemon['pokemon']} with {move}"])
        else: 
            results['significantevents'].append([line[1],f"{pokemon['pokemon']} fainted"])
    return line,parsedlogfile,results

def damager_search(parsedlogfile,line,team,pokemon,results,damagedone):
    damager=None
    move=None
    turndata=list(filter(lambda x: x[1] == line[1] and x[0] < line[0], parsedlogfile))
    turndata=turndata[::-1]
    for line in turndata:
        if team=="p1a":
            if line[2]=="move" and line[3].split(":",1)[0]=="p2a" and line[3].find(f"p1a: {pokemon['pokemon']}")>-1:
                damager=line[3].split(" ",1)[1].split("|",1)[0]
                damager=roster_search("p2a",damager,results)
                damager['damagedone']+=damagedone
                move=line[3].split("|")[1]
        elif team=="p2a":
            if line[2]=="move" and line[3].split(":",1)[0]=="p1a" and line[3].find(f"p2a: {pokemon['pokemon']}")>-1:
                damager=line[3].split(" ",1)[1].split("|",1)[0]
                damager=roster_search("p1a",damager,results)
                damager['damagedone']+=damagedone
                move=line[3].split("|")[1]
    return damager,move

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
    pokemon['hphealed']+=healthhealed
    return line,parsedlogfile,results

def move_function(line,parsedlogfile,results):
    move=line[3].split("|")[1]
    team=line[3].split(":",1)[0]
    #check for support
    #results=supportcheck(results,move,team,line)
    #check for miss
    if line[3].find("|[miss]")>-1:
        line,parsedlogfile,results=miss_function(line,parsedlogfile,results)
    return line,parsedlogfile,results

def supportcheck(results,move,team,line):
    supportmoves=['Reflect','Light Screen','Heal Bell','Aromatherapy','Wish','Stealth Rocks','Spikes','Toxic Spikes','Sticky Web', 'Aurora Veil','Defog','Rapid Spin','Hail','Sandstorm','Sunny Day','Rain Dance','Encore','Taunt','Haze','Clear Smog','Roar','Whirlwind','Leech Seed','Toxic','Will-O-Wisp','Stun Spore','Poison Powder','Block','Mean Look','Dark Void','Destiny Bond','Disable','Electric Terrain','Embargo','Endure','Fairy Lock',"Forest's Curse",'Glare','Grass Whistle','Grassy Terrain','Gravity','Grudge','Heal Block','Healing Wish','Hypnosis','Lucky Chant','Lunar Dance','Magic Coat','Magic Room','Mean Look','Memento','Mist','Misty Terrain','Mud Sport','Parting Shot','Perish Song','Poison Gas','Psychic Terrain','Safeguard','Simple Beam','Sing','Skill Swap','Sleep Powder','Soak','Speed Swap','Spider Web','Spite','Spore','Sweet Kiss','Switcheroo','Tailwind','Thunder Wave','Torment','Toxic Thread','Trick','Trick Room','Water Sport','Wonder Room','Worry Seed','Yawn']
    if move in supportmoves and team=="p1a":
        supportiterator(results,line,'team1',move)
    elif move in supportmoves and team=="p2a":
        supportiterator(results,line,'team1',move)
    return results

def supportiterator(results,line,team,move):
    pokemon=line[3].split(' ',1)[1].split(f"|{move}")[0]
    #searchroster
    pokemon=roster_search(team,pokemon,results)
    print(pokemon)
    pokemon['support']+=1
    results['significantevents'].append([line[1],f"{pokemon['pokemon']} provided support by using {move}"])
    return results,pokemon

def player_function(line,parsedlogfile,results):
    if line[3].split("|",1)[0]=="p1":
        results['team1']['coach']=line[3].split("|")[1]
    elif line[3].split("|",1)[0]=="p2":
        results['team2']['coach']=line[3].split("|")[1]
    return line,parsedlogfile,results

def poke_function(line,parsedlogfile,results):
    if line[3].split("|",1)[0]=="p1":
        results['team1']['roster'].append({
            'pokemon':line[3].split("|")[1], 'startform':line[3].split("|")[1],'nickname':line[3].split("|")[1],
            'kills':0,'deaths':0,'causeofdeath':None,'support':0,'damagedone':0,'hphealed':0,'luck':0,'remaininghealth':100,'lines':[],
        })
    elif line[3].split("|",1)[0]=="p2":
        results['team2']['roster'].append({
            'pokemon':line[3].split("|")[1], 'startform':line[3].split("|")[1],'nickname':line[3].split("|")[1],
            'kills':0,'deaths':0,'causeofdeath':None,'support':0,'damagedone':0,'hphealed':0,'luck':0,'remaininghealth':100,'lines':[],
        })
    return line,parsedlogfile,results

def win_function(line,parsedlogfile,results):
    winner=line[3]
    if winner==results['team1']['coach']:
        results['team1']['wins']=1
    elif winner==results['team2']['coach']:
        results['team2']['wins']=1
    return line,parsedlogfile,results

def switch_drag_function(line,parsedlogfile,results):
    if line[3].split(":",1)[0]=="p1a":
        results,line=namecheck(results,line,1)
    elif line[3].split(":",1)[0]=="p2a":
        results,line=namecheck(results,line,2)
    return line,parsedlogfile,results

def detailschange_function(line,parsedlogfile,results):
    if line[3].split(":",1)[0]=="p1a" and line[3].find("-Mega")>-1:
        results,line=replacemega(results,line,1)
    elif line[3].split(":",1)[0]=="p2a" and line[3].find("-Mega")>-1:
        results,line=replacemega(results,line,2)  
    return line,parsedlogfile,results

def zpower_function(line,parsedlogfile,results):
    if line[3].find("p1a")>-1:
        results['team1']['usedzmove']=True
    elif line[3].find("p2a")>-1:
        results['team2']['usedzmove']=True
    return line,parsedlogfile,results

def message_function(line,parsedlogfile,results):
    if line[3].find("forfeited.")>-1:
        ffcoach=line[3].split(" forfeited.")[0]
        if ffcoach == results['team1']['coach']:
            results['team1']['forfeit']=1
        elif ffcoach == results['team2']['coach']:
                results['team2']['forfeit']=1
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
                item['remaininghealth']=healthremaining
    else:
        if nicknamesearch[1].find("Silvally-")>-1:
            line[3]=line[3].replace(nicknamesearch[1],"Silvally")
            nicknamesearch[1]="Silvally"
        for item in results[f'team{teamnumber}']['roster']:
            if item['pokemon']==nicknamesearch[1] and nicknamesearch[1].find("-Mega")==-1:
                item['startform']=nicknamesearch[0]
                item['nickname']=nicknamesearch[0]
                item['remaininghealth']=healthremaining
    if line[2]=="switch":    
        results[f'team{teamnumber}']['timesswitched']+=1
    return results,line

def replacenames(results,line):
    for item in results[f'team1']['roster']:
        if line.find(item['nickname'])>-1:
            line=line.replace(item['nickname'],item['pokemon'])
        #elif item['pokemon']!=item['startform'] and line.find(f"{item['startform']}-")==-1:
        #    line=line.replace(f"{item['startform']}",f"{item['pokemon']}")
    for item in results[f'team2']['roster']:
        if line.find(item['nickname'])>-1:
            line=line.replace(item['nickname'],item['pokemon'])
        #elif item['pokemon']!=item['startform'] and line.find(f"{item['startform']}-")==-1:
        #    line=line.replace(f"{item['startform']}",f"{item['pokemon']}")
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
    results['numberofturns']=0
    results['turns']=[]
    results['replay']=""
    results['significantevents']=[]
    return results

def roster_search(team,pokemon,results):
    if team=="p1a":
        team="team1"
    elif team=="p2a":
        team="team2"
    for mon in results[team]['roster']:
        if mon['nickname']==pokemon:
            pokemon=mon
    return pokemon