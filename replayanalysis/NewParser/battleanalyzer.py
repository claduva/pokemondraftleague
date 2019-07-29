from .killchecks import *

def gothroughturns(logfile,results):
    turns=results['turns']
    for i in range(len(turns)):
        turndata=turns[i][str(i)]
        for line in turndata:
            #add to line data
            for mon in results['team1']['roster']:
                if line.find(mon['pokemon'])>-1:
                    mon['lines'].append([i,line])
            for mon in results['team2']['roster']:
                if line.find(mon['pokemon'])>-1:
                    mon['lines'].append([i,line])
    #go through mons
    #find cause of deaths
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
    results=forfeitadjustment(results,i)
    #investigate deaths
    for mon in results['team1']['roster']:
        if mon['deaths']==0:
            results['team1']['score']+=1
            remaining=100
            for line in mon['lines']:
                if line[1].find("/100")>-1:
                    remaining=int(line[1].split(f"{mon['pokemon']}|")[-1].split("/")[0])
            mon['remaininghealth']=remaining    
        else:
            results=killersearch(results,mon,results['team1'],2)
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
            results=killersearch(results,mon,results['team2'],1)
            mon['remaininghealth']=0
        results['team2']['remaininghealth']+=mon['remaininghealth']
    results['team1']['remaininghealth']=f"{results['team1']['remaininghealth']}/{100*len(results['team1']['roster'])}"
    results['team2']['remaininghealth']=f"{results['team2']['remaininghealth']}/{100*len(results['team2']['roster'])}"
    return logfile,results

def killersearch(results,mon,roster,otherteam):
    if mon['causeofdeath']=="Direct Damage":
        results=directdamagesearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Burn":
        results=burnsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Poison":
        results=poisonsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Rocky Helmet":
        results=rockyhelmetsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath']=="Perish Song":
        results=perishsongsearch(results,mon,roster,otherteam)
    elif mon['causeofdeath'] in ["Explosion","Self-Destruct","Memento"] :
        if otherteam==1:
            print('here')
            results['team2']['selfdeaths']+=1
        elif otherteam==2:
            results['team1']['selfdeaths']+=1
        deathturn=mon['lines'][-1][0]
        results['significantevents'].append([deathturn,f'{mon["pokemon"]} killed themself with {mon["causeofdeath"]}'])
    return results

def supportcheck():
    supportmoves=['Reflect','Light Screen','Heal Bell','Aromatherapy','Wish','Stealth Rocks','Spikes','Toxic Spikes','Sticky Web', 'Aurora Veil','Defog','Rapid Spin','Hail','Sandstorm','Sunny Day','Rain Dance','Encore','Taunt','Haze','Clear Smog','Roar','Whirlwind','Leech Seed','Toxic','Will-O-Wisp','Stun Spore','Poison Powder','Block','Mean Look','Dark Void','Destiny Bond','Disable','Electric Terrain','Embargo','Endure','Fairy Lock',"Forest's Curse",'Glare','Grass Whistle','Grassy Terrain','Gravity','Grudge','Heal Block','Healing Wish','Hypnosis','Lucky Chant','Lunar Dance','Magic Coat','Magic Room','Mean Look','Memento','Mist','Misty Terrain','Mud Sport','Parting Shot','Perish Song','Poison Gas','Psychic Terrain','Safeguard','Simple Beam','Sing','Skill Swap','Sleep Powder','Soak','Speed Swap','Spider Web','Spite','Spore','Sweet Kiss','Switcheroo','Tailwind','Thunder Wave','Torment','Toxic Thread','Trick','Trick Room','Water Sport','Wonder Room','Worry Seed','Yawn']

def movemissingcheck():
    movesthatcanmiss=[['Precipice Blades', 85], ['High Horsepower', 95], ['Sand Tomb', 85], ['Triple Kick', 90], ['Tail Slap', 85], ['Double Slap', 85], ['Sky Uppercut', 90], ['Super Fang', 90], ['Hyper Beam', 90], ['Dynamic Punch', 50], ['Focus Blast', 70], ['Ice Ball', 90], ['Crush Claw', 95], ['Leech Seed', 90], ['Metal Claw', 95], ['Magma Storm', 75], ['Aeroblast', 95], ['Thunder Wave', 90], ['Head Smash', 80], ['Sing', 55], ['Blizzard', 70], ['Blast Burn', 90], ['Pin Missile', 95], ['Overheat', 90], ['Swagger', 85], ['Flying Press', 95], ['Fly', 95], ['Poison Gas', 90], ['Crabhammer', 90], ['Razor Leaf', 95], ['Poison Powder', 75], ['Rock Tomb', 95], ['Power Whip', 85], ['Supersonic', 55], ['Bind', 85], ['Fissure', 30], ['Sweet Kiss', 75], ['Play Rough', 90], ['Fury Swipes', 80], ['Zen Headbutt', 90], ['Belch', 90], ['Fury Cutter', 95], ['Iron Tail', 75], ['Toxic', 90], ['Egg Bomb', 75], ['Shadow Strike', 95], ['Thunder Fang', 95], ['Charge Beam', 90], ['Lovely Kiss', 75], ['Clamp', 85], ['Rock Throw', 90], ['Ice Fang', 95], ['Electroweb', 95], ['Whirlpool', 85], ['Smog', 70], ['Icy Wind', 95], ['Steel Wing', 90], ['Sonic Boom', 90], ['Hypnosis', 60], ['Fire Fang', 95], ['Seed Flare', 85], ['Hydro Cannon', 90], ['Jump Kick', 95], ['Leaf Storm', 90], ['Bolt Strike', 85], ['Air Cutter', 95], ['Mega Kick', 75], ['Inferno', 50], ['Rock Climb', 85], ['Rock Blast', 90], ['Freeze Shock', 90], ['Drill Run', 95], ['Floaty Fall', 95], ['Fire Spin', 85], ['Frenzy Plant', 90], ['Bone Rush', 90], ['Guillotine', 30], ['Slam', 75], ['Aqua Tail', 90], ['Diamond Storm', 95], ['Metal Sound', 85], ['Psycho Boost', 90], ['Gear Grind', 85], ['Barrage', 85], ['Bonemerang', 90], ['Draco Meteor', 90], ['Leaf Tornado', 90], ['Hyper Fang', 90], ['Muddy Water', 85], ['Thunder', 70], ['Sleep Powder', 75], ['Hammer Arm', 90], ['Origin Pulse', 85], ['Kinesis', 80], ['Grass Whistle', 55], ['Bone Club', 85], ['Fire Blast', 85], ['Mud Bomb', 85], ['Sheer Cold', 30], ['Frost Breath', 90], ['Roar of Time', 90], ['Hydro Pump', 80], ['Fury Attack', 85], ['High Jump Kick', 90], ['Steam Eruption', 95], ['Mega Punch', 85], ['Stun Spore', 75], ['Night Daze', 95], ['Dragon Tail', 90], ['Horn Drill', 30], ['String Shot', 95], ['Ice Hammer', 90], ['V-create', 95], ['Mud Shot', 95], ['Present', 90], ['Mirror Shot', 85], ['Megahorn', 85], ['Screech', 85], ['Sacred Fire', 95], ['Take Down', 85], ['Zap Cannon', 50], ['Octazooka', 85], ['Double Hit', 90], ['Snarl', 95], ['Stone Edge', 80], ['Rock Wrecker', 90], ['Cut', 95], ['Comet Punch', 85], ['Air Slash', 95], ['Fleur Cannon', 90], ['Dragon Rush', 75], ['Submission', 80], ['Circle Throw', 90], ['Bounce', 85], ['Giga Impact', 90], ['Hurricane', 70], ['Ice Burn', 90], ['Cross Chop', 80], ['Gunk Shot', 80], ['Blaze Kick', 90], ['Meteor Mash', 90], ['Dark Void', 50], ['Dual Chop', 90], ['Rollout', 90], ['Wrap', 90], ['Icicle Crash', 90], ['Will-O-Wisp', 85], ['Glaciate', 95], ['Spacial Rend', 95], ['Light of Ruin', 90], ["Nature's Madness", 90], ['Rock Slide', 90], ['Heat Wave', 90], ['Razor Shell', 95], ['Rolling Kick', 85], ['Blue Flare', 85], ['Sky Attack', 90]]

def movesecondaryeffectcheck():
    moveswithsecondaryeffect=[['Thunder Punch', 'par', 10], ['Fire Punch', 'brn', 10], ['Zing Zap', 'flinch', 30], ['Chatter', 'confusion', 100], ['Extrasensory', 'flinch', 10], ['Ice Punch', 'frz', 10], ['Thunder Shock', 'par', 10], ['Dynamic Punch', 'confusion', 100], ['Poison Sting', 'psn', 30], ['Focus Blast', 'boosts spd: -1 ', 10], ['Liquidation', 'boosts def: -1 ', 20], ['Crush Claw', 'boosts def: -1 ', 50], ['Metal Claw', 'self boosts: atk: 1 ', 10], ['Acid', 'boosts spd: -1 ', 10], ['Aurora Beam', 'boosts atk: -1 ', 10], ['Heart Stamp', 'flinch', 30], ['Crunch', 'boosts def: -1 ', 20], ['Water Pulse', 'confusion', 20], ['Acid Spray', 'boosts spd: -2 ', 100], ['Blizzard', 'frz', 10], ['Paleo Wave', 'boosts atk: -1 ', 20], ['Mud-Slap', 'boosts accuracy: -1 ', 100], ['Freeze-Dry', 'frz', 10], ['Flame Charge', 'self boosts: spe: 1 ', 100], ['Dizzy Punch', 'confusion', 20], ['Lunge', 'boosts atk: -1 ', 100], ['Fire Lash', 'boosts def: -1 ', 100], ['Relic Song', 'slp', 10], ['Fake Out', 'flinch', 100], ['Signal Beam', 'confusion', 10], ['Rock Tomb', 'boosts spe: -1 ', 100], ['Buzzy Buzz', 'par', 100], ['Ancient Power', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10], ['Steamroller', 'flinch', 30], ['Bubble Beam', 'boosts spe: -1 ', 10], ['Sludge', 'psn', 30], ['Bulldoze', 'boosts spe: -1 ', 100], ['Play Rough', 'boosts atk: -1 ', 10], ['Astonish', 'flinch', 30], ['Energy Ball', 'boosts spd: -1 ', 10], ['Zen Headbutt', 'flinch', 20], ['Iron Tail', 'boosts def: -1 ', 30], ['Shadow Strike', 'boosts def: -1 ', 50], ['Charge Beam', 'self boosts: spa: 1 ', 70], ['Secret Power', 'par', 30], ['Struggle Bug', 'boosts spa: -1 ', 100], ['Tri Attack', 'par frz or brn', 20], ['Psychic', 'boosts spd: -1 ', 10], ['Electroweb', 'boosts spe: -1 ', 100], ['Smog', 'psn', 40], ['Icy Wind', 'boosts spe: -1 ', 100], ['Steel Wing', 'self boosts: def: 1 ', 10], ['Iron Head', 'flinch', 30], ['Trop Kick', 'boosts atk: -1 ', 100], ['Headbutt', 'flinch', 30], ['Body Slam', 'par', 30], ['Bug Buzz', 'boosts spd: -1 ', 10], ['Seed Flare', 'boosts spd: -2 ', 40], ['Mist Ball', 'boosts spa: -1 ', 50], ['Earth Power', 'boosts spd: -1 ', 10], ['Bolt Strike', 'par', 20], ['Bite', 'flinch', 30], ['Inferno', 'brn', 100], ['Flamethrower', 'brn', 10], ['Rock Climb', 'confusion', 20], ['Freeze Shock', 'par', 30], ['Dark Pulse', 'flinch', 20], ['Flash Cannon', 'boosts spd: -1 ', 10], ['Floaty Fall', 'flinch', 30], ['Poison Fang', 'tox', 50], ['Sludge Bomb', 'psn', 30], ['Lick', 'par', 30], ['Diamond Storm', 'self boosts: def: 2 ', 50], ['Shadow Ball', 'boosts spd: -1 ', 20], ['Cross Poison', 'psn', 10], ['Low Sweep', 'boosts spe: -1 ', 100], ['Sludge Wave', 'psn', 10], ['Leaf Tornado', 'boosts accuracy: -1 ', 50], ['Hyper Fang', 'flinch', 10], ['Muddy Water', 'boosts accuracy: -1 ', 30], ['Thunder', 'par', 30], ['Constrict', 'boosts spe: -1 ', 10], ['Genesis Supernova', 'self  ', 100], ['Stomp', 'flinch', 30], ['Poison Tail', 'psn', 10], ['Bone Club', 'flinch', 10], ['Fire Blast', 'brn', 10], ['Mud Bomb', 'boosts accuracy: -1 ', 30], ['Twineedle', 'psn', 20], ['Splishy Splash', 'par', 30], ['Mystical Fire', 'boosts spa: -1 ', 100], ['Confusion', 'confusion', 10], ['Steam Eruption', 'brn', 30], ['Fiery Dance', 'self boosts: spa: 1 ', 50], ['Night Daze', 'boosts accuracy: -1 ', 40], ['Flare Blitz', 'brn', 10], ['Mud Shot', 'boosts spe: -1 ', 100], ['Mirror Shot', 'boosts accuracy: -1 ', 30], ['Sacred Fire', 'brn', 50], ['Ice Beam', 'frz', 10], ["Magikarp's Revenge", 'confusion', 100], ['Poison Jab', 'psn', 30], ['Double Iron Bash', 'flinch', 30], ['Nuzzle', 'par', 100], ['Zap Cannon', 'par', 100], ['Waterfall', 'flinch', 20], ['Psybeam', 'confusion', 10], ['Octazooka', 'boosts accuracy: -1 ', 50], ['Snarl', 'boosts spa: -1 ', 100], ['Spark', 'par', 30], ['Needle Arm', 'flinch', 30], ['Dragon Breath', 'par', 30], ['Air Slash', 'flinch', 30], ['Dragon Rush', 'flinch', 20], ['Silver Wind', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10], ['Luster Purge', 'boosts spd: -1 ', 50], ['Snore', 'flinch', 30], ['Thunderbolt', 'par', 10], ['Flame Wheel', 'brn', 10], ['Bounce', 'par', 30], ['Scald', 'brn', 30], ['Force Palm', 'par', 30], ['Hurricane', 'confusion', 30], ['Ice Burn', 'brn', 30], ['Gunk Shot', 'psn', 30], ['Blaze Kick', 'brn', 10], ['Lava Plume', 'brn', 30], ['Meteor Mash', 'self boosts: atk: 1 ', 20], ['Searing Shot', 'brn', 30], ['Twister', 'flinch', 20], ['Icicle Crash', 'flinch', 30], ['Bubble', 'boosts spe: -1 ', 10], ['Glaciate', 'boosts spe: -1 ', 100], ['Sizzly Slide', 'brn', 100], ['Rock Smash', 'boosts def: -1 ', 50], ['Volt Tackle', 'par', 10], ['Ember', 'brn', 10], ['Stoked Sparksurfer', 'par', 100], ['Powder Snow', 'frz', 10], ['Power-Up Punch', 'self boosts: atk: 1 ', 100], ['Moonblast', 'boosts spa: -1 ', 30], ['Rock Slide', 'flinch', 30], ['Shadow Bone', 'boosts def: -1 ', 20], ['Heat Wave', 'brn', 10], ['Discharge', 'par', 30], ['Ominous Wind', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10], ['Razor Shell', 'boosts def: -1 ', 50], ['Rolling Kick', 'flinch', 30], ['Blue Flare', 'brn', 20], ['Sky Attack', 'flinch', 30]]

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
                results['team1']['deaths']+=1
                results['team2']['kills']+=1
                killstoadd+=1
                results['significantevents'].append([results['numberofturns'],f'{item["pokemon"]} was killed by {killrecipient["pokemon"]} via forfeit.'])
        print(killstoadd)
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
                results['team2']['deaths']+=1
                results['team1']['kills']+=1
                killstoadd+=1
                results['significantevents'].append([results['numberofturns'],f'{item["pokemon"]} was killed by {killrecipient["pokemon"]} via forfeit.'])
        killrecipient['kills']+=killstoadd
    return results

if __name__ == "__main__":
    main()