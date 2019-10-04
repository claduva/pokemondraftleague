def freezecheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-status|p{otherteam}a: {recipient}|frz")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Freeze Happened')
            break
    return results

def paralysischeck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-status|p{otherteam}a: {recipient}|par")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Paralysis Happened')
            break
    return results

def burncheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-status|p{otherteam}a: {recipient}|brn")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Burn Happened')
            break
    return results

def poisoncheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-status|p{otherteam}a: {recipient}|psn")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Poison Happened')
            break
    return results

def toxiccheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-status|p{otherteam}a: {recipient}|tox")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Toxic Happened')
            break
    return results

def sleepcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-status|p{otherteam}a: {recipient}|slp")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Sleep Happened')
            break
    return results

def flinchcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|cant|p{otherteam}a: {recipient}|flinch")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Flinch Happened')
            break
    return results

def confusioncheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-start|p{otherteam}a: {recipient}|confusion")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Confusion Happened')
            break
    return results

def selfboostcheck(results,remaininglines,turn,item,line,recipient,attacker,thisteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-boost|p{thisteam}a: {attacker}|")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Self Boosts Happened')
            break
    return results

def boostcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-unboost|p{otherteam}a: {recipient}|")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Unboosts Happened')
            break
    return results

def triattackcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect):
    for line_ in remaininglines:
        if line_.find(f"|-status|p{otherteam}a: {recipient}|frz")>-1 or line_.find(f"|-status|p{otherteam}a: {recipient}|brn")>-1 or line_.find(f"|-status|p{otherteam}a: {recipient}|par")>-1:
            team1expectedsecondaryeffect=oddsofeffect
            team2expectedsecondaryeffectagainst=oddsofeffect
            results,attacker=luckiterator(results,attacker,'team1',team1expectedsecondaryeffect)
            results,recipient=luckiterator(results,recipient,'team2',-team2expectedsecondaryeffectagainst)
            #print('Tri Attack Happened')
            break
    return results

def secondarycheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,thisteam,oddsofeffect):
    if item[1]=='frz':  
        results=freezecheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)    
    elif item[1]=='brn':  
        results=burncheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)  
    elif item[1]=='par':  
        results=paralysischeck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)  
    elif item[1]=='psn':  
        results=poisoncheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)  
    elif item[1]=='tox':  
        results=toxiccheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)
    elif item[1]=='slp':  
        results=sleepcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)
    elif item[1]=='flinch':  
        results=flinchcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)
    elif item[1]=='confusion':  
        results=confusioncheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)
    elif item[1].find("self boosts")>-1:
        results=selfboostcheck(results,remaininglines,turn,item,line,recipient,attacker,thisteam,oddsofeffect)
    elif item[1].find("boosts")>-1:
        results=boostcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)
    elif item[1]=='par frz or brn':
        results=triattackcheck(results,remaininglines,turn,item,line,recipient,attacker,otherteam,oddsofeffect)
    return results

def luckiterator(results,pokemon,team,amount):
    for mon in results[team]['roster']:
        if mon['nickname']==pokemon:
            mon['luck']+=amount
            mon['luck']=round(mon['luck'],2)
            pokemon=mon['pokemon']
    return results,pokemon