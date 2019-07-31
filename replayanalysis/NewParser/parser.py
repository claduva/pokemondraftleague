#git submodule foreach git pull origin master
import requests
import json

from .battleanalyzer import *

def newreplayparse(replay):
    #initialize variables
    logfile = requests.get(replay+".log").text.splitlines()
    
    #initialize output json
    results,logfile,removedlines=initializeoutput(logfile)
    results['replay']=replay

    logfile,results=collectturns(logfile,results)

    logfile,results=gothroughturns(logfile,results)

    results['significantevents']=sorted( results['significantevents'],key=lambda tup: tup[0])

    with open('replayanalysis/NewParser/results.json', 'w') as f:
        json.dump(results,f,indent=2)

    open('replayanalysis/NewParser/replaylog.txt', 'wb') 
    with open('replayanalysis/NewParser/replaylog.txt', 'ab') as f: 
        for line in logfile:
            line=f'{line}\n'
            f.write(line.encode(errors="replace"))
    
    open('replayanalysis/NewParser/removedlines.txt', 'wb') 
    with open('replayanalysis/NewParser/removedlines.txt', 'ab') as f: 
        for line in removedlines:
            line=f'{line}\n'
            f.write(line.encode(errors="replace"))
    return results

def main():
    #samplereplay = "https://replay.pokemonshowdown.com/gen7ubers-948905940"
    #samplereplay = "https://replay.pokemonshowdown.com/gen7ou-828150903"
    samplereplay = "http://replay.pokemonshowdown.com/gen7customgame-758459994"
    newreplayparse(samplereplay)

def collectturns(logfile,results):
    i=0
    turn={
        str(0):[],
        }
    logfile_=[]
    for line in logfile:
        #results,line=replacenames(results,line)
        if line.find('|turn|')>-1 and i==0:
            i+=1
            results['turns'].append(turn)
            turn={
                str(i):[],
                }
        elif line.find('|turn|')>-1:
            i+=1
            results['turns'].append(turn)
            turn={
                str(i):[],
                }
        elif line.find('|win|')>-1:
            results['turns'].append(turn)
            winner=line.split("|win|")[1]
            if winner== results['team1']['coach']:
                results['team1']['wins']=1
            elif winner== results['team2']['coach']:
                results['team2']['wins']=1
        else:
            turn[str(i)].append(line)
        logfile_.append(line)
    results['numberofturns']=len(results['turns'])-1
    return logfile_,results

def initializeoutput(logfile):
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

    logfile_=[]
    removedlines=[]
    removelist=["|","|teampreview","|start","|clearpoke","|upkeep"]
    for line in logfile:
        line=line.replace(", M","").replace(", F","").replace("-*","").replace(", shiny","")
        #replace nicknames
        #results,line=replacenames(results,line)
        #find coaches
        if line.find('|player|p1|')>-1:
            results['team1']['coach']=line.split("|")[3]
            removedlines.append(line)
        elif line.find('|player|p2|')>-1:
            results['team2']['coach']=line.split("|")[3]
            removedlines.append(line)
        #find teams
        elif line.find('|poke|p1|')>-1:
            results['team1']['roster'].append({
                'pokemon':line.split("|")[3],
                'startform':line.split("|")[3],
                'nickname':line.split("|")[3],
                'kills':0,
                'deaths':0,
                'causeofdeath':None,
                'support':0,
                'damagedone':0,
                'hphealed':0,
                'luck':0,
                'remaininghealth':100,
                'lines':[],
                })
            removedlines.append(line)
        elif line.find('|poke|p2|')>-1:
            results['team2']['roster'].append({
                'pokemon':line.split("|")[3],
                'startform':line.split("|")[3],
                'nickname':line.split("|")[3],
                'kills':0,
                'deaths':0,
                'causeofdeath':None,
                'support':0,
                'damagedone':0,
                'hphealed':0,
                'luck':0,
                'remaininghealth':100,
                'lines':[],
                })
            removedlines.append(line)
        #check names
        elif line.find("|switch|p1a:")>-1 or line.find("|drag|p1a:")>-1:
            results,line,logfile_=namecheck(results,line,1,logfile_)
        elif line.find("|switch|p2a:")>-1 or line.find("|drag|p2a:")>-1:
            results,line,logfile_=namecheck(results,line,2,logfile_)
        #replace mega
        elif line.find("|detailschange|p1a:")>-1 and line.find("-Mega")>-1:
            results,line,removedlines=replacemega(results,line,1,removedlines)
        elif line.find("|detailschange|p2a:")>-1 and line.find("-Mega")>-1:
            results,line,removedlines=replacemega(results,line,2,removedlines)
        #check z
        elif line.find("|-zpower|p1a")>-1:
            results['team1']['usedzmove']=True
            removedlines.append(line)
        elif line.find("|-zpower|p2a")>-1:
            results['team2']['usedzmove']=True
            removedlines.append(line)
        #check forfeit
        elif line.find("|-message|")>-1 and line.find("forfeited.")>-1:
            ffcoach=line.split(" forfeited.")[0].split("|-message|",1)[1]
            if ffcoach == results['team1']['coach']:
                results['team1']['forfeit']=1
            elif ffcoach == results['team2']['coach']:
                results['team2']['forfeit']=1
            removedlines.append(line)
        elif line in removelist or line.find('|j|')>-1 or line.find('|c|')>-1 or line.find('|l|')>-1 or \
            line.find('|teamsize|')>-1 or line.find('|gen|')>-1 or line.find('|gametype|')>-1 or \
            line.find('|tier|')>-1 or line.find('|rule|')>-1 or line.find("|-mega|p1a")>-1 or line.find("|-mega|p2a")>-1 or \
            line.find("|seed|")>-1 or line.find("|teampreview|")>-1:
            removedlines.append(line)
        else:
            logfile_.append(line) 
    return results,logfile_,removedlines

def namecheck(results,line,teamnumber,logfile):
    nicknamesearch=line.split(" ",1)[1].split("|")
    if nicknamesearch[0]!=nicknamesearch[1] and nicknamesearch[1].find(f"{nicknamesearch[0]}-")==-1:
        if nicknamesearch[1].find("Silvally-")>-1:
            line=line.replace(nicknamesearch[1],"Silvally")
            nicknamesearch[1]="Silvally"
        for item in results[f'team{teamnumber}']['roster']:
            if item['pokemon']==nicknamesearch[1]:
                item['nickname']=nicknamesearch[0]
                #line=line.replace(nicknamesearch[0],nicknamesearch[1])
    else:
        if nicknamesearch[1].find("Silvally-")>-1:
            line=line.replace(nicknamesearch[1],"Silvally")
            nicknamesearch[1]="Silvally"
        for item in results[f'team{teamnumber}']['roster']:
            if item['pokemon']==nicknamesearch[1] and nicknamesearch[1].find("-Mega")==-1:
                item['startform']=nicknamesearch[0]
                item['nickname']=nicknamesearch[0]
            #line=line.replace(f'{nicknamesearch[0]}|',f'{nicknamesearch[1]}|')
    logfile.append(line)
    if line.find(f"|switch|p{teamnumber}a:")>-1:    
        results[f'team{teamnumber}']['timesswitched']+=1
    return results,line,logfile

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

def replacemega(results,line,teamnumber,removedlines):
    results[f'team{teamnumber}']['megaevolved']=True
    removedlines.append(line)
    megasearch=line.split(" ",1)[1].split("|")
    for item in results[f'team{teamnumber}']['roster']:
        if item['pokemon']==megasearch[0] or item['nickname']==megasearch[0]:
            item['pokemon']=megasearch[1]
    #line=line.replace(megasearch[0],megasearch[1])
    return results,line,removedlines

if __name__ == "__main__":
    main()