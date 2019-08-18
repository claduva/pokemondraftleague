
def directdamagesearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["nickname"]}|0 fnt')>-1 or line.find(f'{mon["nickname"]}|0 slp')>-1 or line.find(f'{mon["nickname"]}|0 tox')>-1 or line.find(f'{mon["nickname"]}|0 psn')>-1 or line.find(f'{mon["nickname"]}|0')>-1:
            searchlist=mon['lines'][0:i][::-1]
            for turn_,line_ in searchlist:
                if line_.find(f"|move|p{otherteam}a: ")>-1:
                    killer=line_.split(" ",1)[1].split("|")[0]
                    deathturn=turn_
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([deathturn,f'{mon["pokemon"]} was killed by {killer}.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break
        i+=1
    return results

def poisonsearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["nickname"]}|0 fnt|[from] psn')>-1:
            searchlist=mon['lines'][0:i][::-1]
            j=0
            for turn_,line_ in searchlist:
                if line_.find(f'{mon["nickname"]}|tox')>-1 and line_.find('|-status|')>-1 and searchlist[j+1][1].find(f"|move|p{otherteam}a:")>-1:
                    killer=searchlist[j+1][1].split(" ",1)[1].split("|")[0]
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([searchlist[j+1][0],f'{mon["pokemon"]} was toxiced by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to toxic.'])
                    break
                elif line_.find(f'{mon["nickname"]}|psn')>-1 and line_.find('|-status|')>-1 and searchlist[j+2][1].find(f"|move|p{otherteam}a:")>-1:
                    killer=searchlist[j+2][1].split(" ",1)[1].split("|")[0]
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([searchlist[j+2][0],f'{mon["pokemon"]} was poisoned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to poison.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break
                elif line_.find(f'{mon["nickname"]}|psn')>-1 and line_.find('|[from] ability:')>-1 and line_.find(f'|[of] p{otherteam}a')>-1:
                    killer=line_.split(f'p{otherteam}a: ')[1]
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([turn_,f'{mon["pokemon"]} was poisoned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to poison.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break    
                elif line_.find(f'{mon["nickname"]}|tox')>-1 and line_.find('|-status|')>-1:
                    turnofinterest=results['turns'][turn_][str(turn_)]
                    k=0
                    for line__ in turnofinterest:
                        if line__.find(f"|-status|p{otherteam}a: ")>-1 and turnofinterest[k+1].find(f"|-activate|p{otherteam}a: ")>-1 and turnofinterest[k+1].find(f"|ability: Synchronize")>-1:
                            killer=turnofinterest[k+1].split(" ",1)[1].split("|")[0]
                            results,killer=killiterator(results,otherteam,killer)
                            results['significantevents'].append([searchlist[j+1][0],f'{mon["pokemon"]} was toxiced by {killer} via Syncronize.'])
                            results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to toxic via Syncronize.'])
                        k+=1
                    break
                j+=1
        if line.find(f'{mon["nickname"]}|0 fnt|[from] tox')>-1:
            searchlist=mon['lines'][0:i][::-1]
            j=0
            for turn_,line_ in searchlist:
                if False:
                    pass
                elif line_.find(f'{mon["nickname"]}|tox')>-1 and line_.find('|-status|')>-1 and searchlist[j+2][1].find(f"|move|p{otherteam}a:")>-1:
                    killer=searchlist[j+2][1].split(" ",1)[1].split("|")[0]
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([searchlist[j+2][0],f'{mon["pokemon"]} was poisoned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to poison.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break
                elif line_.find(f'{mon["nickname"]}|tox')>-1 and line_.find('|[from] ability:')>-1 and line_.find(f'|[of] p{otherteam}a')>-1:
                    print(line_)
                    killer=line_.split(f'p{otherteam}a: ')[1]
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([turn_,f'{mon["pokemon"]} was poisoned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to poison.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break    
                j+=1
        i+=1
    return results

def burnsearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["nickname"]}|0 fnt|[from] brn')>-1:
            searchlist=mon['lines'][0:i][::-1]
            j=0
            for turn_,line_ in searchlist:
                if False:
                    pass
                elif line_.find(f'{mon["nickname"]}|brn')>-1 and line_.find('|-status|')>-1 and searchlist[j+2][1].find(f"|move|p{otherteam}a:")>-1:
                    killer=searchlist[j+2][1].split(" ",1)[1].split("|")[0]
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([searchlist[j+2][0],f'{mon["pokemon"]} was burnt by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to burn.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break
                elif line_.find(f'{mon["nickname"]}|brn')>-1 and line_.find('|[from] ability:')>-1 and line_.find(f'|[of] p{otherteam}a')>-1:
                    killer=line_.split(f'p{otherteam}a: ')[1]
                    results,killer=killiterator(results,otherteam,killer)
                    results['significantevents'].append([turn_,f'{mon["pokemon"]} was burned by {killer}.'])
                    results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to burn.'])
                    #print(f'{mon["pokemon"]}: {killer}')
                    break    
                j+=1
        i+=1

    return results

def rockyhelmetsearch(results,mon,roster,otherteam):
    i=0
    killer=None
    for turn,line in mon['lines']:
        if line.find(f'{mon["nickname"]}|0 fnt|[from] item: Rocky Helmet')>-1:
            killer=line.split(f'p{otherteam}a: ')[1]
            results,killer=killiterator(results,otherteam,killer)
            results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} due to Rocky Helmet.'])
        i+=1
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
        if line.find(f'{mon["nickname"]}|perish0')>-1:
            searchlist=unseperatedlines[0:i][::-1]
            for turn_,line_ in searchlist:
                if line_.find("|move|")>-1 and line_.find("|Perish Song|")>-1:
                    setter=line_.split(" ")[-1]
                    if mon['nickname']!=setter:
                        killer=setter
                        results,killer=killiterator(results,otherteam,killer)
                        results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} with Perish Song.'])
                    else:
                        if otherteam==1:
                            results['team2']['selfdeaths']+=1
                        elif otherteam==2:
                            results['team1']['selfdeaths']+=1
                        results['significantevents'].append([turn,f'{mon["pokemon"]} killed itself with Perish Song'])
                    break
        i+=1
    return results

def blacksludgesearch(results,mon,roster,otherteam):
    killer=None
    unseperatedlines=[]
    for i in range(len(results['turns'])):
        for line in results['turns'][i][str(i)]:
            unseperatedlines.append([i,line])
    i=0
    for turn,line in unseperatedlines:
        if line.find(f'|0|[from] item: Black Sludge')>-1:
            searchlist=unseperatedlines[0:i][::-1]
            for turn_,line_ in searchlist:
                if line_.find("|Black Sludge|[from] move:")>-1:
                    setter=line_.split(" ",1)[1].split("|")[0]
                    if mon['nickname']!=setter:
                        killer=setter
                        results,killer=killiterator(results,otherteam,killer)
                        results['significantevents'].append([turn,f'{mon["pokemon"]} was killed by {killer} with Black Sludge.'])
                    else:
                        if otherteam==1:
                            results['team2']['selfdeaths']+=1
                        elif otherteam==2:
                            results['team1']['selfdeaths']+=1
                        results['significantevents'].append([turn,f'{mon["pokemon"]} killed itself with Black Sludge'])
                    break
        i+=1
    return results

def weathersearch(results,mon,roster,otherteam):
    return results

def killiterator(results,otherteam,killer):
    for mon in results[f'team{otherteam}']['roster']:
        if mon['nickname']==killer:
            mon['kills']+=1
            results[f'team{otherteam}']['kills']+=1
            killer=mon['pokemon']
    return results,killer