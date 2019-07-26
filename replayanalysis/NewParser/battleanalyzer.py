def gothroughturns(logfile,results):
    turns=results['turns']
    for i in range(len(turns)):
        turndata=turns[i][str(i)]
        index=0
        for line in turndata:
            #add to line data
            for mon in results['team1']['roster']:
                if line.find(mon['pokemon'])>-1:
                    mon['lines'].append([i,line])
            for mon in results['team2']['roster']:
                if line.find(mon['pokemon'])>-1:
                    mon['lines'].append([i,line])
            #check for deaths
            index+=1
    results=forfeitadjustment(results,i)
    #go through mons
    for mon in results['team1']['roster']:
        index=0
        lines_=[]
        causeofdeathlines=[]
        for line in mon['lines']:
            if line[1].split(" ",1)[1].split("|")[0].find(mon['pokemon'])>-1:
                causeofdeathlines.append(line)
        for line in causeofdeathlines:
            results=checkdeath(line[1],results,index,causeofdeathlines)
            index+=1
    for mon in results['team2']['roster']:
        index=0
        lines_=[]
        causeofdeathlines=[]
        for line in mon['lines']:
            if line[1].split(" ",1)[1].split("|")[0].find(mon['pokemon'])>-1:
                causeofdeathlines.append(line)
        for line in causeofdeathlines:
            results=checkdeath(line[1],results,index,causeofdeathlines)
            index+=1
    for mon in results['team1']['roster']:
        if mon['deaths']==0:
            results['team1']['score']+=1
            remaining=100
            for line in mon['lines']:
                if line[1].find("/100")>-1:
                    remaining=int(line[1].split(f"{mon['pokemon']}|")[-1].split("/")[0])
            mon['remaininghealth']=remaining    
        else:
            mon['remaininghealth']=0
        results['team1']['remaininghealth']+=mon['remaininghealth']
    for mon in results['team2']['roster']:
        if mon['deaths']==0:
            results['team2']['score']+=1
            remaining=100
            for line in mon['lines']:  
                if line[1].find("/100")>-1:
                    remaining=int(line[1].split(f"{mon['pokemon']}|")[-1].split("/100")[0])
            mon['remaininghealth']=remaining    
        else:
            mon['remaininghealth']=0
        results['team2']['remaininghealth']+=mon['remaininghealth']
    results['team1']['remaininghealth']=f"{results['team1']['remaininghealth']}/{100*len(results['team1']['roster'])}"
    results['team2']['remaininghealth']=f"{results['team2']['remaininghealth']}/{100*len(results['team2']['roster'])}"
    return logfile,results

def checkdeath(line,results,index,turndata):
    if line.find('|faint|p1a')>-1:
        fainted=line.split(" ",1)[1]
        #find cause of death
        causeofdeathline=turndata[index-1][1]
        print(line)
        print(causeofdeathline)
        causeofdeath=findcauseofdeath(causeofdeathline)
        for item in results[f'team1']['roster']:
            if item['pokemon']==fainted:
                item['deaths']=1
                item['causeofdeath']=causeofdeath
                results['team1']['deaths']+=1
    elif line.find('|faint|p2a')>-1:
        fainted=line.split(" ",1)[1]
        #find cause of death
        causeofdeathline=turndata[index-1][1]
        print(line)
        print(causeofdeathline)
        causeofdeath=findcauseofdeath(causeofdeathline)
        for item in results[f'team2']['roster']:
            if item['pokemon']==fainted:
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
    elif causeofdeathline.find('perish0')>-1:
        causeofdeath="Perish Song"
    elif causeofdeathline.find('Explosion')>-1:
        causeofdeath="Explosion"
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
            if item_['pokemon']==team2lastmon:
                killrecipient=item_
        killstoadd=0
        for item in results[f'team1']['roster']:
            if item['deaths']!=1:
                item['deaths']=1
                item['causeofdeath']="Forfeit"
                killstoadd+=1
        killrecipient['kills']+=killstoadd
    elif results['team2']['forfeit']==1:
        for item_ in results[f'team1']['roster']:
            if item_['pokemon']==team1lastmon:
                killrecipient=item_
        killstoadd=0
        for item in results[f'team2']['roster']:
            if item['deaths']!=1:
                item['deaths']=1
                item['causeofdeath']="Forfeit"
                killstoadd+=1
        killrecipient['kills']+=killstoadd
    return results

if __name__ == "__main__":
    main()