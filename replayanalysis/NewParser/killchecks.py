
def directdamagesearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["pokemon"]}|0 fnt')>-1:
            searchlist=mon['lines'][0:i][::-1]
            for turn_,line_ in searchlist:
                if line_.find(f"|move|p{otherteam}a: ")>-1:
                    killer=line_.split(" ",1)[1].split("|")[0]
                    deathturn=turn_
                    results['significantevents'].append([deathturn,f'{mon["pokemon"]} was killed by {killer}.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break
        i+=1
    if killer:    
        results=killiterator(results,otherteam,killer)
    return results

def poisonsearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["pokemon"]}|0 fnt|[from] psn')>-1:
            searchlist=mon['lines'][0:i][::-1]
            j=0
            for turn_,line_ in searchlist:
                if False:
                    pass
                elif line_.find(f'{mon["pokemon"]}|psn')>-1 and line_.find('|-status|')>-1 and searchlist[j+2][1].find(f"|move|p{otherteam}a:")>-1:
                    killer=searchlist[j+2][1].split(" ",1)[1].split("|")[0]
                    results['significantevents'].append([searchlist[j+2][0],f'{mon["pokemon"]} was poisoned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to poison.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break
                elif line_.find(f'{mon["pokemon"]}|psn')>-1 and line_.find('|[from] ability:')>-1 and line_.find(f'|[of] p{otherteam}a')>-1:
                    killer=line_.split(" ")[-1]
                    results['significantevents'].append([turn_,f'{mon["pokemon"]} was poisoned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to poison.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break    
                j+=1
        i+=1
    if killer:
        results=killiterator(results,otherteam,killer)
    return results

def burnsearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["pokemon"]}|0 fnt|[from] brn')>-1:
            searchlist=mon['lines'][0:i][::-1]
            j=0
            for turn_,line_ in searchlist:
                if False:
                    pass
                elif line_.find(f'{mon["pokemon"]}|brn')>-1 and line_.find('|-status|')>-1 and searchlist[j+2][1].find(f"|move|p{otherteam}a:")>-1:
                    killer=searchlist[j+2][1].split(" ",1)[1].split("|")[0]
                    results['significantevents'].append([searchlist[j+2][0],f'{mon["pokemon"]} was burnt by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to burn.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break
                elif line_.find(f'{mon["pokemon"]}|brn')>-1 and line_.find('|[from] ability:')>-1 and line_.find(f'|[of] p{otherteam}a')>-1:
                    killer=line_.split(" ")[-1]
                    results['significantevents'].append([turn_,f'{mon["pokemon"]} was burned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to burn.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break    
                j+=1
        i+=1
    if killer:
        results=killiterator(results,otherteam,killer)
    return results

def rockyhelmetsearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["pokemon"]}|0 fnt|[from] item: Rocky Helmet')>-1:
            killer=line.split(" ")[-1]
            results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to Rocky Helmet.'])
        i+=1
    if killer:
        results=killiterator(results,otherteam,killer)
    return results

def trappingmovesearch(results,mon,roster,otherteam):
    return results

def perishsongsearch(results,mon,roster,otherteam):
    killer=None
    unseperatedlines=[]
    for i in range(len(results['turns'])):
        for line in results['turns'][i][str(i)]:
            unseperatedlines.append([i,line])
    i=0
    for turn,line in unseperatedlines:
        if line.find(f'{mon["pokemon"]}|perish0')>-1:
            searchlist=unseperatedlines[0:i][::-1]
            for turn_,line_ in searchlist:
                if line_.find("|move|")>-1 and line_.find("|Perish Song|")>-1:
                    setter=line_.split(" ")[-1]
                    if mon['pokemon']!=setter:
                        killer=setter
                        results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} with Perish Song.'])
                    else:
                        if otherteam==1:
                            results['team2']['selfdeaths']+=1
                        elif otherteam==1:
                            results['team1']['selfdeaths']+=1
                        results['significantevents'].append([turn,f'{mon["pokemon"]} killed itself with Perish Song'])
                    break
        i+=1
    if killer:
        results=killiterator(results,otherteam,killer)
    return results

def weathersearch(results,mon,roster,otherteam):
    return results

def killiterator(results,otherteam,killer):
    for mon in results[f'team{otherteam}']['roster']:
        if mon['pokemon']==killer:
            mon['kills']+=1
            results[f'team{otherteam}']['kills']+=1
    return results