#git submodule foreach git pull origin master
import requests

debugparser=False
if debugparser==False:
    from .replayparsingfunctions import *
    from .killchecks import *
else: 
    from replayparsingfunctions import *
    from killchecks import *

def replayparse(replay):
    #initialize variables
    byline = requests.get(replay+".log").text.splitlines()
    nickname="placeholder"; t1roster=[]; t2roster=[]; indicestoremove=[]; team1=team(); team2=team()

    for i in range(len(byline)):
        #remove unneeded lines
        removeunneededlines(byline,indicestoremove,i)
        #find rosters
        findrosters(byline,team1,team2,t1roster,t2roster,indicestoremove,i)
        #find coachs
        findcoachs(byline,team1,team2,indicestoremove,i)

    #remove unneeded lines
    for i in range(len(indicestoremove)):
        byline.pop(indicestoremove[i]-i)

    for i in range(len(byline)):
        #check for fainted mons and kills
        if byline[i].find("|faint|") > -1:
            fainted=byline[i].split(" ",1)[1]
            
            #check deaths
            deathcheck(byline,fainted,team1,team2,i)
            
            #check kills
            checkkills(byline,team1,team2,fainted,i)
            
    for i in range(len(byline)):
        #check if z move used
        checkz(byline,team1,team2,i)

        #check if mega evolved
        checkmega(byline,team1,team2,i)

    #calculate differentials
    calcdiff(team1,team2)

    #find winner and score
    checkwinner(byline,team1,team2)

    #prepare output string
    outputstring=prepareoutput(replay,byline,team1,team2,i)
    if debugparser==False:
        #write output file
        with open('test.txt', 'wb') as f:
            f.write(outputstring.encode(errors="replace"))

    return outputstring, team1, team2 
    
def main():
    samplereplay = "http://replay.pokemonshowdown.com/gen7ou-869906570"

    #theo vs amir: "https://replay.pokemonshowdown.com/gen7anythinggoes-877334345"
    #clad vs lernes: "http://replay.pokemonshowdown.com/gen7ubers-861263418"
    #hail, spiky sheild, spikes, leech seed, poison, toxic, burn http://replay.pokemonshowdown.com/gen7ou-869896858
    #aftermath http://replay.pokemonshowdown.com/draftfrontier-gen7anythinggoes-45013
    #rocky helmet, iron barbs, sandstorm forfeit http://replay.pokemonshowdown.com/gen7ou-869902579
    #destiny bond, curse http://replay.pokemonshowdown.com/gen7ou-869900570
    #confusion from hurricane https://replay.pokemonshowdown.com/gen7anythinggoes-869449974
    #solar power, dry skin forfeit http://replay.pokemonshowdown.com/gen7ou-869906570

    replaydata,team1,team2=replayparse(samplereplay)

    

if __name__ == "__main__":
    main()