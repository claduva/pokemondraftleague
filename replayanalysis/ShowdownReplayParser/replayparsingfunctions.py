def findcoachs(rawdata,team1,team2,indicestoremove,i):  
    if rawdata[i].find("|player|p1|") > -1:
        coachraw=rawdata[i].split("|")
        team1.coach=coachraw[3]
        indicestoremove.append(i)
    elif rawdata[i].find("|player|p2|") > -1:
        coachraw=rawdata[i].split("|")
        team2.coach=coachraw[3]
        indicestoremove.append(i)

def findrosters(rawdata,team1,team2,t1roster,t2roster,indicestoremove,i):
    member="placeholder123"; nickname="nickname123"
    if rawdata[i].find("|poke|p1|") > -1:
        member=rawdata[i].split("|")[3]
        member.replace(", L50","")
        if member.find("-") > -1 and (member.find("Landorus") == -1 and member.find("Ho-Oh") == -1 and member.find("Shaymin") == -1 and member.find("Greninja") == -1 and member.find("Necrozma") == -1 and member.find("Deoxys") == -1 and member.find("Primal") == -1 and member.find("Rotom") == -1 and member.find("Thundurus") == -1 and member.find("Hoopa") == -1 and member.find("Tornadus") == -1 and member.find("Zygarde") == -1 and member.find("Kyurem") == -1 and member.find("Alola") == -1 and member.find("o-o") == -1 and member.find("Eternal") == -1 and member.find("Porygon") == -1 and member.find("Lycanroc") == -1):   
            member=member.split("-")[0]
        if member.find("Type: Null") > -1:   
            member="Type:Null"
        indicestoremove.append(i)
        t1roster.append(member)
        if len(t1roster)==1:
            team1.pokemon1=member
        if len(t1roster)==2:
            team1.pokemon2=member
        if len(t1roster)==3:
            team1.pokemon3=member
        if len(t1roster)==4:
            team1.pokemon4=member
        if len(t1roster)==5:
            team1.pokemon5=member
        if len(t1roster)==6:
            team1.pokemon6=member
    elif rawdata[i].find("|poke|p2|") > -1:
        member=rawdata[i].split("|")[3]
        if member.find("-") > -1 and (member.find("Landorus") == -1 and member.find("Ho-Oh") == -1 and member.find("Shaymin") == -1 and member.find("Greninja") == -1 and member.find("Necrozma") == -1 and member.find("Deoxys") == -1 and member.find("Primal") == -1 and member.find("Rotom") == -1 and member.find("Thundurus") == -1 and member.find("Hoopa") == -1 and member.find("Tornadus") == -1 and member.find("Zygarde") == -1 and member.find("Kyurem") == -1 and member.find("Alola") == -1 and member.find("o-o") == -1 and member.find("Eternal") == -1 and member.find("Porygon") == -1 and member.find("Lycanroc") == -1):   
            member=member.split("-")[0]
        if member.find("Type: Null") > -1:   
            member="Type:Null"
        indicestoremove.append(i)
        t2roster.append(member)
        if len(t2roster)==1:
            team2.pokemon1=member
        if len(t2roster)==2:
            team2.pokemon2=member
        if len(t2roster)==3:
            team2.pokemon3=member
        if len(t2roster)==4:
            team2.pokemon4=member
        if len(t2roster)==5:
            team2.pokemon5=member
        if len(t2roster)==6:
            team2.pokemon6=member
    for i in range(len(rawdata)):
        if (rawdata[i].find("|"+member) > -1) and ((rawdata[i].find("|switch|") > -1) or (rawdata[i].find("|drag|") > -1)) or (rawdata[i].find("|"+member) > -1 and rawdata[i].find("|replace|") > -1):            
            nickname=rawdata[i].split(" ",1)[1].split("|",1)[0]
            break
    for i in range(len(rawdata)):
        if rawdata[i].find(nickname+"-") ==-1:
            rawdata[i]=rawdata[i].replace(nickname,member)
        rawdata[i]=rawdata[i].replace(member + "|" + member,member)   

def removeunneededlines(rawdata,indicestoremove,i):  
    if (rawdata[i].find("|j|") > -1) or (rawdata[i].find("|c|") > -1) or (rawdata[i].find("|teamsize|") > -1) \
    or (rawdata[i].find("|gen|") > -1) or (rawdata[i].find("|gametype|") > -1) or (rawdata[i].find("|teampreview") > -1) \
    or (rawdata[i].find("|rule|") > -1) or (rawdata[i].find("|tier|") > -1) or (rawdata[i].find("|start") > -1) \
    or (rawdata[i].find("|upkeep") > -1) or (rawdata[i].find("|clearpoke") > -1) or (len(rawdata[i]) == 1) \
    or (rawdata[i].find("|n|") > -1) or (rawdata[i].find("|raw|") > -1) or (rawdata[i].find("|-boost|") > -1) \
    or (rawdata[i].find("|-unboost|") > -1) or (rawdata[i].find("|-ability|") > -1)or (len(rawdata[i]) == 0) \
    or (rawdata[i].find("|l|") > -1) or (rawdata[i].find("|-crit|") > -1) or (rawdata[i].find("|-activate|") > -1) \
    or (rawdata[i].find("|-heal|") > -1) or (rawdata[i].find("|-miss|") > -1) or (rawdata[i].find("|-resisted|") > -1) \
    or (rawdata[i].find("|-supereffective|") > -1) or (rawdata[i].find("|-immune|") > -1) or (rawdata[i].find("|-zbroken|") > -1) \
    or (rawdata[i].find("|-singleturn|") > -1) or (rawdata[i].find("|-enditem|") > -1) or (rawdata[i].find("|-fieldend|") > -1) \
    or (rawdata[i].find("|-fieldstart|") > -1) or (rawdata[i].find("|cant|") > -1) or (rawdata[i].find("|-curestatus|") > -1) \
    or (rawdata[i].find("|-fail|") > -1) or (rawdata[i].find("|-mustrecharge|") > -1) or (rawdata[i].find("|-hitcount|") > -1) \
    or (rawdata[i].find("|-transform|") > -1) or (rawdata[i].find("|debug|") > -1) or ((rawdata[i].find("/100 brn|[from] brn") > -1)) or ((rawdata[i].find("/100 psn|[from] psn") > -1)):
        indicestoremove.append(i)
    rawdata[i]=rawdata[i].replace(", M", "")
    rawdata[i]=rawdata[i].replace(", F", "")
    rawdata[i]=rawdata[i].replace(", shiny", "")
    rawdata[i]=rawdata[i].replace("|item", "|")
    rawdata[i]=rawdata[i].replace(", L50", "")

def deathcheck(rawdata,fainted,team1,team2,i):
    if (rawdata[i].find("p1a") > -1):
        if (team1.pokemon1 == fainted):
            team1.P1F = 1
        elif team1.pokemon2 == fainted:
           team1.P2F = 1
        elif team1.pokemon3 == fainted:
            team1.P3F = 1
        elif team1.pokemon4 == fainted:
            team1.P4F = 1
        elif team1.pokemon5 == fainted:
            team1.P5F = 1
        elif team1.pokemon6 == fainted: 
            team1.P6F = 1
    elif (rawdata[i].find("p2a") > -1):
        if (team2.pokemon1 == fainted):
            team2.P1F = 1
        elif team2.pokemon2 == fainted:
           team2.P2F = 1
        elif team2.pokemon3 == fainted:
            team2.P3F = 1
        elif team2.pokemon4 == fainted:
            team2.P4F = 1
        elif team2.pokemon5 == fainted:
            team2.P5F = 1
        elif team2.pokemon6 == fainted: 
            team2.P6F = 1

def checkz(rawdata,team1,team2,i):
    if rawdata[i].find("zeffect") > -1:
            zuser=rawdata[i].split("|")[2]
            if (zuser.find("p1a") > -1):
                team1.usedz=True
            if (zuser.find("p2a") > -1):
                team2.usedz=True

def checkmega(rawdata,team1,team2,i):
    if rawdata[i].find("-mega") > -1:
            try:
                premega=rawdata[i-1].split("|")[2].split(" ")[1].split("-")[0]
                mega=rawdata[i-1].split(" ")[1]
            except:
                premega=rawdata[i+1].split("|")[2].split(" ")[1].split("-")[0]
                mega=rawdata[i+1].split(" ")[1]
            if (rawdata[i].find("p1a") > -1):
                team1.megaevolved=True
                if team1.pokemon1 == premega:
                    team1.pokemon1 = mega
                elif team1.pokemon2 == premega:
                    team1.pokemon2 = mega
                elif team1.pokemon3 == premega:
                    team1.pokemon3 = mega
                elif team1.pokemon4 == premega:
                    team1.pokemon4 = mega
                elif team1.pokemon5 == premega:
                    team1.pokemon5 = mega
                elif team1.pokemon6 == premega: 
                    team1.pokemon6 = mega
            if (rawdata[i].find("p2a") > -1):
                team2.megaevolved=True
                if team2.pokemon1 == premega:
                    team2.pokemon1 = mega
                elif team2.pokemon2 == premega:
                    team2.pokemon2 = mega
                elif team2.pokemon3 == premega:
                    team2.pokemon3 = mega
                elif team2.pokemon4 == premega:
                    team2.pokemon4 = mega
                elif team2.pokemon5 == premega:
                    team2.pokemon5 = mega
                elif team2.pokemon6 == premega: 
                    team2.pokemon6 = mega

def calcdiff(team1,team2):
    team1.P1Diff=team1.P1K-team1.P1F
    team1.P2Diff=team1.P2K-team1.P2F
    team1.P3Diff=team1.P3K-team1.P3F
    team1.P4Diff=team1.P4K-team1.P4F
    team1.P5Diff=team1.P5K-team1.P5F
    team1.P6Diff=team1.P6K-team1.P6F
    team2.P1Diff=team2.P1K-team2.P1F
    team2.P2Diff=team2.P2K-team2.P2F
    team2.P3Diff=team2.P3K-team2.P3F
    team2.P4Diff=team2.P4K-team2.P4F
    team2.P5Diff=team2.P5K-team2.P5F
    team2.P6Diff=team2.P6K-team2.P6F

def checkwinner(rawdata,team1,team2):
    winningcoach=rawdata[len(rawdata)-1].split("|")[2]
    if winningcoach == team1.coach:
        team1.win=1
    elif winningcoach == team2.coach:
        team2.win=1
    team1.score=6-(team1.P1F+team1.P2F+team1.P3F+team1.P4F+team1.P5F+team1.P6F)
    team2.score=6-(team2.P1F+team2.P2F+team2.P3F+team2.P4F+team2.P5F+team2.P6F)
    if rawdata[len(rawdata)-2].find("forfeited")>-1:
        if team1.win==1:
            team2.diff=-6
            team2.score=0
            team2.forfeit=1
            team2.P1F=1
            team2.P2F=1
            team2.P3F=1
            team2.P4F=1
            team2.P5F=1
            team2.P6F=1
            lastmon="placeholder"
            j=1
            while lastmon=="placeholder":
                if rawdata[len(rawdata)-2-j].find("|move|p1a:")>-1:
                    lastmon=rawdata[len(rawdata)-2-j].split(" ",1)[1].split("|")[0]
                j+=1
            for i in range(6-team1.P1K-team1.P2K-team1.P3K-team1.P4K-team1.P5K-team1.P6K):    
                incrementkills(team1,lastmon) 
                redodiff(team1,lastmon)   
        elif team2.win==1:
            team1.diff=-6
            team1.score=0
            team1.forfeit=1
            team1.P1F=1
            team1.P2F=1
            team1.P3F=1
            team1.P4F=1
            team1.P5F=1
            team1.P6F=1
            lastmon="placeholder"
            j=1
            while lastmon=="placeholder":
                if rawdata[len(rawdata)-2-j].find("|move|p2a:")>-1:
                    lastmon=rawdata[len(rawdata)-2-j].split(" ",1)[1].split("|")[0]
                j+=1
            for i in range(6-team2.P1K-team2.P2K-team2.P3K-team2.P4K-team2.P5K-team2.P6K):    
                incrementkills(team2,lastmon)  
                redodiff(team2,lastmon)  
    else:
        if team1.win==1:
            team1.diff=team1.score
            team2.diff=-team1.diff
        elif team2.win==1:
            team2.diff=team2.score
            team1.diff=-team2.diff

def prepareoutput(replay,rawdata,team1,team2,i):
    outputstring="Team 1 Coach: " + str(team1.coach) + "\nTeam 1 Roster: \n" +str(team1.pokemon1) + \
        ", Kills: " + str(team1.P1K) + ", Deaths: " + str(team1.P1F) +  ", +/-: " + str(team1.P1Diff) + "\n" + \
        str(team1.pokemon2) + ", Kills: " + str(team1.P2K) +  ", Deaths: " +  str(team1.P2F) + ", +/-: " + \
        str(team1.P2Diff) + "\n" + str(team1.pokemon3) + ", Kills: " + str(team1.P3K) +  ", Deaths: " + \
        str(team1.P3F) +  ", +/-: " + str(team1.P3Diff) + "\n" + str(team1.pokemon4) + ", Kills: " + \
        str(team1.P4K) + ", Deaths: " +  str(team1.P4F) + ", +/-: " + str(team1.P4Diff) + "\n" + str(team1.pokemon5) + \
        ", Kills: " +  str(team1.P5K) + ", Deaths: " +  str(team1.P5F) + ", +/-: " + str(team1.P5Diff) + "\n" + \
        str(team1.pokemon6) + ", Kills: " + str(team1.P6K) +  ", Deaths: " +  str(team1.P6F) + ", +/-: " + \
        str(team1.P6Diff) + "\nMega Evolved: " + str(team1.megaevolved) + "\nUsed Z-Move: " + str(team1.usedz) + "\n\n" + \
        "Team 2 Coach: " + str(team2.coach) + "\nTeam 2 Roster: \n" +str(team2.pokemon1) + \
        ", Kills: " + str(team2.P1K) + ", Deaths: " + str(team2.P1F) +  ", +/-: " + str(team2.P1Diff) + "\n" + \
        str(team2.pokemon2) + ", Kills: " + str(team2.P2K) +  ", Deaths: " +  str(team2.P2F) + ", +/-: " + \
        str(team2.P2Diff) + "\n" + str(team2.pokemon3) + ", Kills: " + str(team2.P3K) +  ", Deaths: " + \
        str(team2.P3F) +  ", +/-: " + str(team2.P3Diff) + "\n" + str(team2.pokemon4) + ", Kills: " +  \
        str(team2.P4K) + ", Deaths: " +  str(team2.P4F) + ", +/-: " + str(team2.P4Diff) + "\n" + str(team2.pokemon5) + \
        ", Kills: " +  str(team2.P5K) + ", Deaths: " +  str(team2.P5F) + ", +/-: " + str(team2.P5Diff) + "\n" + \
        str(team2.pokemon6) + ", Kills: " + str(team2.P6K) +  ", Deaths: " +  str(team2.P6F) + ", +/-: " + \
        str(team2.P6Diff) + "\nMega Evolved: " + str(team2.megaevolved) + "\nUsed Z-Move: " + str(team2.usedz) + "\n\n"
    #for i in range(len(rawdata)):
    #    outputstring=outputstring + rawdata[i] + "\n"
    outputstring=outputstring + "Replay: " + str(replay) + "\n"
    return outputstring

class team:
    def __init__(self):
        self.team=""
        self.coach=""
        self.pokemon1=""
        self.pokemon2=""
        self.pokemon3=""
        self.pokemon4=""
        self.pokemon5=""
        self.pokemon6=""
        self.P1F=0
        self.P2F=0
        self.P3F=0
        self.P4F=0
        self.P5F=0
        self.P6F=0
        self.P1K=0
        self.P2K=0
        self.P3K=0
        self.P4K=0
        self.P5K=0
        self.P6K=0
        self.P1Diff=0
        self.P2Diff=0
        self.P3Diff=0
        self.P4Diff=0
        self.P5Diff=0
        self.P6Diff=0
        self.megaevolved=False
        self.usedz=False
        self.luck=0
        self.win=0
        self.score=0
        self.diff=0
        self.forfeit=0

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

def redodiff(team,killer):
    if team.pokemon1 ==killer:
        team.P1Diff = team.P1K-team.P1F
    elif team.pokemon2 == killer:
        team.P2Diff = team.P2K-team.P2F
    elif team.pokemon3 == killer:
        team.P3Diff = team.P3K-team.P3F
    elif team.pokemon4 == killer:
        team.P4Diff = team.P4K-team.P4F
    elif team.pokemon5 == killer:
        team.P5Diff = team.P5K-team.P5F
    elif team.pokemon6 == killer:
        team.P6Diff = team.P6K-team.P6F

if __name__ == "__main__":
    main()