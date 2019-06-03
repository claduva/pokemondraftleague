def directdamagekill(rawdata,team,i):
    destinybondcondition=(rawdata[i-4].find("|-singlemove|")==-1) # and (rawdata[i-4].find("Destiny Bond")>-1)
    otherconditions=(rawdata[i-1].find("[from] Hail") == -1) and (rawdata[i-1].find("[from] Leech Seed") == -1) \
        and (rawdata[i-1].find("[from] Stealth Rock") == -1) and (rawdata[i-1].find("[from] Spikes") == -1) \
        and (rawdata[i-1].find("[from] psn")==-1) and (rawdata[i-1].find("[from] brn") == -1) and (rawdata[i-2].find("fnt|[from] ability: Aftermath") == -1) \
        and (rawdata[i-1].find("[from] recoil")==-1)  and (rawdata[i-1].find("fnt|[from] ability: Iron Barbs")==-1)  and (rawdata[i-1].find("fnt|[from] ability: Rough Skin")==-1) \
        and (rawdata[i-1].find("fnt|[from] item: Rocky Helmet")==-1) and (rawdata[i-1].find("Sandstorm")==-1) and (rawdata[i-1].find("Hail")==-1) \
        and (rawdata[i-1].find("[from] confusion")== -1) and (rawdata[i-1].find("[from] Curse")==-1) and (rawdata[i-1].find("Solar Power")==-1) \
        and (rawdata[i-1].find("Dry Skin")==-1) and destinybondcondition        
    if (rawdata[i-2].find("|move|") > -1) and otherconditions:
        killer=rawdata[i-2].split(" ",1)[1]
        killer=killer.split("|",1)[0]
        incrementkills(team,killer)
    elif (rawdata[i-3].find("|move|") > -1) and otherconditions:
        killer=rawdata[i-3].split(" ",1)[1]
        killer=killer.split("|",1)[0]
        incrementkills(team,killer)
    elif (rawdata[i-4].find("|move|") > -1) and otherconditions:
        killer=rawdata[i-4].split(" ",1)[1]
        killer=killer.split("|",1)[0]
        incrementkills(team,killer)     
    elif (rawdata[i-5].find("|move|") > -1) and otherconditions:
        killer=rawdata[i-5].split(" ",1)[1]
        killer=killer.split("|",1)[0]
        incrementkills(team,killer)
    elif (rawdata[i-6].find("|move|") > -1) and otherconditions:
        killer=rawdata[i-6].split(" ",1)[1]
        killer=killer.split("|",1)[0]
        incrementkills(team,killer)
    elif (rawdata[i-7].find("|move|") > -1) and otherconditions:
        killer=rawdata[i-7].split(" ",1)[1]
        killer=killer.split("|",1)[0]
        incrementkills(team,killer)  

def contacteffectkill(rawdata,team,fainted,i):
    if ((rawdata[i-1].find("item: Rocky Helmet") > -1) or (rawdata[i-1].find("ability: Iron Barbs") > -1) \
    or (rawdata[i-1].find("ability: Rough Skin") > -1)  or (rawdata[i-1].find("[from] Spiky Shield") > -1)) \
    and (rawdata[i-1].find("|-damage|") > -1): 
        killer=rawdata[i-1].split(" ")[-1]
        if fainted != killer:
            incrementkills(team,killer)

def leechseedkill(rawdata,team,fainted,i):
    if (rawdata[i-1].find("[from] Leech Seed") > -1) and (rawdata[i-1].find("|-damage|") > -1): 
        killer="placeholder"; j=1
        while(killer=="placeholder"):
            if  (rawdata[i-j].find("|move|") > -1) and (rawdata[i-j].find("Leech Seed|") > -1):
                killer=rawdata[i-j].split(" ",1)[1].split("|")[0]
            j+=1
        incrementkills(team,killer)

def aftermathkill(rawdata,team,fainted,i):
    if (rawdata[i-2].find("[from] ability: Aftermath") > -1) and (rawdata[i-2].find("|-damage|") > -1): 
        killer=rawdata[i-2].split(" ")[-1]
        if fainted != killer:
            incrementkills(team,killer)

def hazardskill(rawdata,team,fainted,player,i):
    if (rawdata[i-1].find("[from] Stealth Rock") > -1): 
        killer="placeholder"; j=1
        while(killer=="placeholder"):
            if  (rawdata[i-j].find("sidestart|p"+player) > -1) and (rawdata[i-j].find("Stealth Rock") > -1):
                killer=rawdata[i-j-1].split(" ",1)[1].split("|")[0]
            j+=1
        incrementkills(team,killer)
    elif (rawdata[i-1].find("[from] Spikes") > -1): 
        killer="placeholder"; j=1
        while(killer=="placeholder"):
            if  (rawdata[i-j].find("sidestart|p"+player) > -1) and (rawdata[i-j].find("Spikes") > -1):
                killer=rawdata[i-j-1].split(" ",1)[1].split("|")[0]
            j+=1
        incrementkills(team,killer)

def weatherkill(rawdata,team,fainted,player,otherplayer,i):
    if (rawdata[i-1].find("[from] Hail") > -1): 
        killer="placeholder"; j=1
        while(killer=="placeholder" and (i-j)>=0):
            #from ability
            if  (rawdata[i-j].find("-weather|Hail|") > -1) and (rawdata[i-j].find("[of] "+player) > -1):
                killer=rawdata[i-j].split(" ")[-1]
            #from move
            elif  (rawdata[i-j].find("Hail") > -1) and (rawdata[i-j].find("move|"+otherplayer) > -1):
                killer=rawdata[i-j].split(" ",1)[1].split("|")[0]
            j+=1
        incrementkills(team,killer)
    elif (rawdata[i-1].find("[from] Sandstorm") > -1): 
        killer="placeholder"; j=1
        while(killer=="placeholder" and (i-j)>=0):
            #from ability
            if  (rawdata[i-j].find("-weather|Sandstorm|[from] ability: Sand Stream|[of]") > -1) and (rawdata[i-j].find(otherplayer) > -1):
                killer=rawdata[i-j].split(" ",5)[5]
            #from move
            elif  (rawdata[i-j].find("Sandstorm") > -1) and (rawdata[i-j].find("move|"+otherplayer) > -1):
                print('move')
                killer=rawdata[i-j].split(" ",1)[1].split("|")[0]
            j+=1
        incrementkills(team,killer)
   
def poisonkill(rawdata,team,player,fainted,i):
    if (rawdata[i-1].find("[from] psn") > -1) and (rawdata[i-1].find("|-damage|"+player) > -1): 
        killer="placeholder"; j=2
        while(killer=="placeholder" and (i-j)>=0):
            #toxic status
            if (rawdata[i-j].find("|tox") > -1) and (rawdata[i-j].find("|-status|"+player) > -1)  and (rawdata[i-j].find(fainted) > -1):
                #toxic the move
                if (rawdata[i-j-1].find("move") > -1):
                    killer=rawdata[i-j-1].split(" ",1)[1].split("|")[0]
                #secondary effect
                elif ((rawdata[i-j-1].find("damage") > -1) and (rawdata[i-j-1].find("[from]") == -1)):
                    killer=rawdata[i-j-2].split(" ",1)[1].split("|")[0]
                #toxic spikes
                else:
                    k=1;
                    while(killer=="placeholder"):
                        if  (rawdata[i-j-k].find("sidestart|"+player[0:1]) > -1) and (rawdata[i-j-k].find("Toxic Spikes") > -1):
                            killer=rawdata[i-j-k-1].split(" ",1)[1].split("|")[0]
                        k+=1
            #psn status
            if (rawdata[i-j].find("|psn") > -1) and (rawdata[i-j].find("|-status|"+player) > -1)  and (rawdata[i-j].find(fainted) > -1):
                #direct move
                if (rawdata[i-j-1].find("move") > -1):
                    killer=rawdata[i-j-1].split(" ",1)[1].split("|")[0]
                #secondary effect
                if ((rawdata[i-j-1].find("damage") > -1) and (rawdata[i-j-1].find("[from]") == -1)):
                    killer=rawdata[i-j-2].split(" ",1)[1].split("|")[0]
                #toxic spikes
                else:
                    k=1;
                    while(killer=="placeholder"):
                        if  (rawdata[i-j-k].find("sidestart|"+player[0:1]) > -1) and (rawdata[i-j-k].find("Toxic Spikes") > -1):
                            killer=rawdata[i-j-k-1].split(" ",1)[1].split("|")[0]
                        k+=1
            j+=1
        incrementkills(team,killer)

def burnkill(rawdata,team,player,fainted,i):
    if ((rawdata[i-1].find("[from] brn") > -1) and (rawdata[i-1].find("|-damage|"+player) > -1)) or ((rawdata[i-2].find("[from] brn") > -1) and (rawdata[i-2].find("|-damage|"+player) > -1)): 
        killer="placeholder"; j=2
        while(killer=="placeholder" and (i-j)>=0):
            if (rawdata[i-j].find("|brn") > -1) and (rawdata[i-j].find("|-status|"+player) > -1)  and (rawdata[i-j].find(fainted) > -1):
                #burn the move
                if (rawdata[i-j-1].find("move") > -1):
                    killer=rawdata[i-j-1].split(" ",1)[1].split("|")[0]
                #secondary effect
                elif ((rawdata[i-j-1].find("damage") > -1) and (rawdata[i-j-1].find("[from]") == -1)):
                    killer=rawdata[i-j-2].split(" ",1)[1].split("|")[0]
            j+=1
        incrementkills(team,killer)

def destinybondkill(rawdata,team,player,fainted,i):
      if (rawdata[i-1].find("faint") > -1) and (rawdata[i-4].find("Destiny Bond") > -1) and (rawdata[i-4].find(player) > -1): 
        killer=rawdata[i-4].split(" ",1)[1].split("|")[0]
        if fainted != killer:
            incrementkills(team,killer)

def cursekill(rawdata,team,player,fainted,i):
      if (rawdata[i-1].find("[from] Curse") > -1) and (rawdata[i-1].find("|-damage|") > -1): 
        killer="placeholder"; j=2
        while(killer=="placeholder"):
            #from ability
            if  (rawdata[i-j].find("-start|") > -1) and (rawdata[i-j].find(fainted+"|Curse") > -1):
                killer=rawdata[i-j-1].split(" ",1)[1].split("|")[0]
            j+=1
            if fainted != killer:
                incrementkills(team,killer)

def confusionkill(rawdata,team,player,fainted,i):
      if (rawdata[i-1].find("[from] confusion") > -1) and (rawdata[i-1].find("|-damage|") > -1): 
        killer="placeholder"; j=2
        while(killer=="placeholder"):
            #direct
            if  (rawdata[i-j].find("-start|") > -1) and (rawdata[i-j].find("confusion") > -1):
                if rawdata[i-j-1].find("-damage|")>-1:
                #secondary effect
                    killer=rawdata[i-j-2].split(" ",1)[1].split("|")[0]
                #direct
                else:
                    killer=rawdata[i-j-1].split(" ",1)[1].split("|")[0]
            j+=1
            if fainted != killer:
                incrementkills(team,killer)

def checkkills(byline,team1,team2,fainted,i):
    if (byline[i].find("p2a") > -1):
        #kill belongs to team 1
        directdamagekill(byline,team1,i)
        contacteffectkill(byline,team1,fainted,i)
        leechseedkill(byline,team1,fainted,i)
        aftermathkill(byline,team1,fainted,i)
        hazardskill(byline,team1,fainted,"2",i)
        weatherkill(byline,team1,fainted,"p2a","p1a",i)
        poisonkill(byline,team1,"p2a",fainted,i)
        burnkill(byline,team1,"p2a",fainted,i)
        destinybondkill(byline,team1,"p1a",fainted,i)
        cursekill(byline,team1,"p2a",fainted,i)
        confusionkill(byline,team1,"p2a",fainted,i)
    elif (byline[i].find("p1a") > -1):
        #kill belongs to team 2
        directdamagekill(byline,team2,i)
        contacteffectkill(byline,team2,fainted,i)
        leechseedkill(byline,team2,fainted,i)
        aftermathkill(byline,team2,fainted,i)
        hazardskill(byline,team2,fainted,"1",i)
        weatherkill(byline,team2,fainted,"p1a","p2a",i)
        poisonkill(byline,team2,"p1a",fainted,i)
        burnkill(byline,team2,"p1a",fainted,i)
        destinybondkill(byline,team2,"p2a",fainted,i)
        cursekill(byline,team2,"p1a",fainted,i)
        confusionkill(byline,team2,"p1a",fainted,i)

def incrementkills(team,killer):
    if team.pokemon1 ==killer:
        team.P1K += 1
    elif team.pokemon2 == killer:
        team.P2K += 1
    elif team.pokemon3 == killer:
        team.P3K += 1
    elif team.pokemon4 == killer:
        team.P4K += 1
    elif team.pokemon5 == killer:
        team.P5K += 1
    elif team.pokemon6 == killer:
        team.P6K += 1
    
if __name__ == "__main__":
    main()