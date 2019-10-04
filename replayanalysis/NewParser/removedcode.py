""" 
    logfile,results=collectturns(logfile,results)
    logfile,results=gothroughturns(logfile,results)
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
             """

def main():
    #samplereplay = "https://replay.pokemonshowdown.com/gen7ubers-948905940"
    #samplereplay = "https://replay.pokemonshowdown.com/gen7ou-828150903"
    samplereplay = "http://replay.pokemonshowdown.com/gen7customgame-758459994"
    newreplayparse(samplereplay)

if __name__ == "__main__":
    main()
