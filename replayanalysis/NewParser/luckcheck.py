from .secondaryeffects import *

def luckcheck(results,turndata,turn):
    results=misscheck(results,turndata,turn)
    results=critcheck(results,turndata,turn)
    results=secondaryeffectcheck(results,turndata,turn)
    results['team1']['luck']=round(results['team1']['luck'],2)
    results['team2']['luck']=round(results['team2']['luck'],2)
    return results

def secondaryeffectcheck(results,turndata,turn):
    moveswithsecondaryeffect=[['Thunder Punch', 'par', 10], ['Fire Punch', 'brn', 10], ['Zing Zap', 'flinch', 30], ['Chatter', 'confusion', 100], ['Extrasensory', 'flinch', 10], ['Ice Punch', 'frz', 10], ['Thunder Shock', 'par', 10], ['Dynamic Punch', 'confusion', 100], ['Poison Sting', 'psn', 30], ['Focus Blast', 'boosts spd: -1 ', 10], ['Liquidation', 'boosts def: -1 ', 20], ['Crush Claw', 'boosts def: -1 ', 50], ['Metal Claw', 'self boosts: atk: 1 ', 10], ['Acid', 'boosts spd: -1 ', 10], ['Aurora Beam', 'boosts atk: -1 ', 10], ['Heart Stamp', 'flinch', 30], ['Crunch', 'boosts def: -1 ', 20], ['Water Pulse', 'confusion', 20], ['Acid Spray', 'boosts spd: -2 ', 100], ['Blizzard', 'frz', 10], ['Paleo Wave', 'boosts atk: -1 ', 20], ['Mud-Slap', 'boosts accuracy: -1 ', 100], ['Freeze-Dry', 'frz', 10], ['Flame Charge', 'self boosts: spe: 1 ', 100], ['Dizzy Punch', 'confusion', 20], ['Lunge', 'boosts atk: -1 ', 100], ['Fire Lash', 'boosts def: -1 ', 100], ['Relic Song', 'slp', 10], ['Fake Out', 'flinch', 100], ['Signal Beam', 'confusion', 10], ['Rock Tomb', 'boosts spe: -1 ', 100], ['Buzzy Buzz', 'par', 100], ['Ancient Power', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10], ['Steamroller', 'flinch', 30], ['Bubble Beam', 'boosts spe: -1 ', 10], ['Sludge', 'psn', 30], ['Bulldoze', 'boosts spe: -1 ', 100], ['Play Rough', 'boosts atk: -1 ', 10], ['Astonish', 'flinch', 30], ['Energy Ball', 'boosts spd: -1 ', 10], ['Zen Headbutt', 'flinch', 20], ['Iron Tail', 'boosts def: -1 ', 30], ['Shadow Strike', 'boosts def: -1 ', 50], ['Charge Beam', 'self boosts: spa: 1 ', 70], ['Secret Power', 'par', 30], ['Struggle Bug', 'boosts spa: -1 ', 100], ['Tri Attack', 'par frz or brn', 20], ['Psychic', 'boosts spd: -1 ', 10], ['Electroweb', 'boosts spe: -1 ', 100], ['Smog', 'psn', 40], ['Icy Wind', 'boosts spe: -1 ', 100], ['Steel Wing', 'self boosts: def: 1 ', 10], ['Iron Head', 'flinch', 30], ['Trop Kick', 'boosts atk: -1 ', 100], ['Headbutt', 'flinch', 30], ['Body Slam', 'par', 30], ['Bug Buzz', 'boosts spd: -1 ', 10], ['Seed Flare', 'boosts spd: -2 ', 40], ['Mist Ball', 'boosts spa: -1 ', 50], ['Earth Power', 'boosts spd: -1 ', 10], ['Bolt Strike', 'par', 20], ['Bite', 'flinch', 30], ['Inferno', 'brn', 100], ['Flamethrower', 'brn', 10], ['Rock Climb', 'confusion', 20], ['Freeze Shock', 'par', 30], ['Dark Pulse', 'flinch', 20], ['Flash Cannon', 'boosts spd: -1 ', 10], ['Floaty Fall', 'flinch', 30], ['Poison Fang', 'tox', 50], ['Sludge Bomb', 'psn', 30], ['Lick', 'par', 30], ['Diamond Storm', 'self boosts: def: 2 ', 50], ['Shadow Ball', 'boosts spd: -1 ', 20], ['Cross Poison', 'psn', 10], ['Low Sweep', 'boosts spe: -1 ', 100], ['Sludge Wave', 'psn', 10], ['Leaf Tornado', 'boosts accuracy: -1 ', 50], ['Hyper Fang', 'flinch', 10], ['Muddy Water', 'boosts accuracy: -1 ', 30], ['Thunder', 'par', 30], ['Constrict', 'boosts spe: -1 ', 10], ['Genesis Supernova', 'self  ', 100], ['Stomp', 'flinch', 30], ['Poison Tail', 'psn', 10], ['Bone Club', 'flinch', 10], ['Fire Blast', 'brn', 10], ['Mud Bomb', 'boosts accuracy: -1 ', 30], ['Twineedle', 'psn', 20], ['Splishy Splash', 'par', 30], ['Mystical Fire', 'boosts spa: -1 ', 100], ['Confusion', 'confusion', 10], ['Steam Eruption', 'brn', 30], ['Fiery Dance', 'self boosts: spa: 1 ', 50], ['Night Daze', 'boosts accuracy: -1 ', 40], ['Flare Blitz', 'brn', 10], ['Mud Shot', 'boosts spe: -1 ', 100], ['Mirror Shot', 'boosts accuracy: -1 ', 30], ['Sacred Fire', 'brn', 50], ['Ice Beam', 'frz', 10], ["Magikarp's Revenge", 'confusion', 100], ['Poison Jab', 'psn', 30], ['Double Iron Bash', 'flinch', 30], ['Nuzzle', 'par', 100], ['Zap Cannon', 'par', 100], ['Waterfall', 'flinch', 20], ['Psybeam', 'confusion', 10], ['Octazooka', 'boosts accuracy: -1 ', 50], ['Snarl', 'boosts spa: -1 ', 100], ['Spark', 'par', 30], ['Needle Arm', 'flinch', 30], ['Dragon Breath', 'par', 30], ['Air Slash', 'flinch', 30], ['Dragon Rush', 'flinch', 20], ['Silver Wind', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10], ['Luster Purge', 'boosts spd: -1 ', 50], ['Snore', 'flinch', 30], ['Thunderbolt', 'par', 10], ['Flame Wheel', 'brn', 10], ['Bounce', 'par', 30], ['Scald', 'brn', 30], ['Force Palm', 'par', 30], ['Hurricane', 'confusion', 30], ['Ice Burn', 'brn', 30], ['Gunk Shot', 'psn', 30], ['Blaze Kick', 'brn', 10], ['Lava Plume', 'brn', 30], ['Meteor Mash', 'self boosts: atk: 1 ', 20], ['Searing Shot', 'brn', 30], ['Twister', 'flinch', 20], ['Icicle Crash', 'flinch', 30], ['Bubble', 'boosts spe: -1 ', 10], ['Glaciate', 'boosts spe: -1 ', 100], ['Sizzly Slide', 'brn', 100], ['Rock Smash', 'boosts def: -1 ', 50], ['Volt Tackle', 'par', 10], ['Ember', 'brn', 10], ['Stoked Sparksurfer', 'par', 100], ['Powder Snow', 'frz', 10], ['Power-Up Punch', 'self boosts: atk: 1 ', 100], ['Moonblast', 'boosts spa: -1 ', 30], ['Rock Slide', 'flinch', 30], ['Shadow Bone', 'boosts def: -1 ', 20], ['Heat Wave', 'brn', 10], ['Discharge', 'par', 30], ['Ominous Wind', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 10], ['Razor Shell', 'boosts def: -1 ', 50], ['Rolling Kick', 'flinch', 30], ['Blue Flare', 'brn', 20], ['Sky Attack', 'flinch', 30]]
    #['confusion','boosts spd: -1 ', 'boosts def: -1 ', 'self boosts: atk: 1 ', 'boosts atk: -1 ', 'boosts spd: -2 ', 'boosts accuracy: -1 ', 'self boosts: spe: 1 ','boosts spe: -1 ', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', 'self boosts: spa: 1 ', 'boosts spa: -1 ', 'par frz or brn', 'self boosts: def: 1 ','self boosts: def: 2 ', 'self  ']
    team1expectedsecondaryeffect=0
    for item in moveswithsecondaryeffect:
        if item[1]=='self  ':
            print(item[0])
    team2expectedsecondaryeffect=0
    team1expectedsecondaryeffectagainst=0
    team2expectedsecondaryeffectagainst=0
    team1secondaryeffect=0
    team2secondaryeffect=0
    team1secondaryeffectagainst=0
    team2secondaryeffectagainst=0
    i=0
    for line in turndata:
        if line.find("|move|p1a:")>-1 and line.find("|p2a:")>-1:
            move=line.split(" ",1)[1].split("|")[1]
            if [item for item in moveswithsecondaryeffect if item[0] == move]:
                attacker=line.split(" ",1)[1].split('|')[0]
                recipient=line.split("p2a: ",1)[1].split('|')[0]
                item=[item for item in moveswithsecondaryeffect if item[0] == move][0]
                oddsofeffect=round(item[2]/100,2)
                remaininglines=turndata[i+1:]
                results=secondarycheck(results,remaininglines,turn,item,line,recipient,2)                    
        if line.find("|move|p2a:")>-1 and line.find("|p1a:")>-1:
            move=line.split(" ",1)[1].split("|")[1]
            if [item for item in moveswithsecondaryeffect if item[0] == move]:
                attacker=line.split(" ",1)[1].split('|')[0]
                recipient=line.split("p1a: ",1)[1].split('|')[0]
                item=[item for item in moveswithsecondaryeffect if item[0] == move][0]
                oddsofeffect=round(item[2]/100,2)
                remaininglines=turndata[i+1:]
                results=secondarycheck(results,remaininglines,turn,item,line,recipient,1)  
        i+=1
    results['team1']['luck']+=team1secondaryeffectagainst-team1secondaryeffect+team1expectedsecondaryeffect-team1expectedsecondaryeffectagainst
    results['team2']['luck']+=team2secondaryeffectagainst-team2secondaryeffect+team2expectedsecondaryeffect-team2expectedsecondaryeffectagainst
    return results

def misscheck(results,turndata,turn):
    movesthatcanmiss=[['Precipice Blades', 85], ['High Horsepower', 95], ['Sand Tomb', 85], ['Triple Kick', 90], ['Tail Slap', 85], ['Double Slap', 85], ['Sky Uppercut', 90], ['Super Fang', 90], ['Hyper Beam', 90], ['Dynamic Punch', 50], ['Focus Blast', 70], ['Ice Ball', 90], ['Crush Claw', 95], ['Leech Seed', 90], ['Metal Claw', 95], ['Magma Storm', 75], ['Aeroblast', 95], ['Thunder Wave', 90], ['Head Smash', 80], ['Sing', 55], ['Blizzard', 70], ['Blast Burn', 90], ['Pin Missile', 95], ['Overheat', 90], ['Swagger', 85], ['Flying Press', 95], ['Fly', 95], ['Poison Gas', 90], ['Crabhammer', 90], ['Razor Leaf', 95], ['Poison Powder', 75], ['Rock Tomb', 95], ['Power Whip', 85], ['Supersonic', 55], ['Bind', 85], ['Fissure', 30], ['Sweet Kiss', 75], ['Play Rough', 90], ['Fury Swipes', 80], ['Zen Headbutt', 90], ['Belch', 90], ['Fury Cutter', 95], ['Iron Tail', 75], ['Toxic', 90], ['Egg Bomb', 75], ['Shadow Strike', 95], ['Thunder Fang', 95], ['Charge Beam', 90], ['Lovely Kiss', 75], ['Clamp', 85], ['Rock Throw', 90], ['Ice Fang', 95], ['Electroweb', 95], ['Whirlpool', 85], ['Smog', 70], ['Icy Wind', 95], ['Steel Wing', 90], ['Sonic Boom', 90], ['Hypnosis', 60], ['Fire Fang', 95], ['Seed Flare', 85], ['Hydro Cannon', 90], ['Jump Kick', 95], ['Leaf Storm', 90], ['Bolt Strike', 85], ['Air Cutter', 95], ['Mega Kick', 75], ['Inferno', 50], ['Rock Climb', 85], ['Rock Blast', 90], ['Freeze Shock', 90], ['Drill Run', 95], ['Floaty Fall', 95], ['Fire Spin', 85], ['Frenzy Plant', 90], ['Bone Rush', 90], ['Guillotine', 30], ['Slam', 75], ['Aqua Tail', 90], ['Diamond Storm', 95], ['Metal Sound', 85], ['Psycho Boost', 90], ['Gear Grind', 85], ['Barrage', 85], ['Bonemerang', 90], ['Draco Meteor', 90], ['Leaf Tornado', 90], ['Hyper Fang', 90], ['Muddy Water', 85], ['Thunder', 70], ['Sleep Powder', 75], ['Hammer Arm', 90], ['Origin Pulse', 85], ['Kinesis', 80], ['Grass Whistle', 55], ['Bone Club', 85], ['Fire Blast', 85], ['Mud Bomb', 85], ['Sheer Cold', 30], ['Frost Breath', 90], ['Roar of Time', 90], ['Hydro Pump', 80], ['Fury Attack', 85], ['High Jump Kick', 90], ['Steam Eruption', 95], ['Mega Punch', 85], ['Stun Spore', 75], ['Night Daze', 95], ['Dragon Tail', 90], ['Horn Drill', 30], ['String Shot', 95], ['Ice Hammer', 90], ['V-create', 95], ['Mud Shot', 95], ['Present', 90], ['Mirror Shot', 85], ['Megahorn', 85], ['Screech', 85], ['Sacred Fire', 95], ['Take Down', 85], ['Zap Cannon', 50], ['Octazooka', 85], ['Double Hit', 90], ['Snarl', 95], ['Stone Edge', 80], ['Rock Wrecker', 90], ['Cut', 95], ['Comet Punch', 85], ['Air Slash', 95], ['Fleur Cannon', 90], ['Dragon Rush', 75], ['Submission', 80], ['Circle Throw', 90], ['Bounce', 85], ['Giga Impact', 90], ['Hurricane', 70], ['Ice Burn', 90], ['Cross Chop', 80], ['Gunk Shot', 80], ['Blaze Kick', 90], ['Meteor Mash', 90], ['Dark Void', 50], ['Dual Chop', 90], ['Rollout', 90], ['Wrap', 90], ['Icicle Crash', 90], ['Will-O-Wisp', 85], ['Glaciate', 95], ['Spacial Rend', 95], ['Light of Ruin', 90], ["Nature's Madness", 90], ['Rock Slide', 90], ['Heat Wave', 90], ['Razor Shell', 95], ['Rolling Kick', 85], ['Blue Flare', 85], ['Sky Attack', 90]]
    team1expectedmiss=0
    team2expectedmiss=0
    team1expectedmissagainst=0
    team2expectedmissagainst=0
    team1miss=0
    team2miss=0
    team1missagainst=0
    team2missagainst=0
    for line in turndata:
        if line.find("|move|p1a:")>-1 and line.find("|p2a:")>-1:
            move=line.split(" ",1)[1].split("|")[1]
            if [item for item in movesthatcanmiss if item[0] == move]:
                attacker=line.split(" ",1)[1].split('|')[0]
                recipient=line.split("p2a: ",1)[1].split('|')[0]
                oddsofmiss=round(1-[item[1] for item in movesthatcanmiss if item[0] == move][0]/100,2)
                team1expectedmiss=oddsofmiss
                team2expectedmissagainst=oddsofmiss
                results,attacker=luckiterator(results,attacker,'team1',team1expectedmiss)
                results,recipient=luckiterator(results,recipient,'team2',-team2expectedmissagainst)
        if line.find("|move|p2a:")>-1 and line.find("|p1a:")>-1:
            move=line.split(" ",1)[1].split("|")[1]
            if [item for item in movesthatcanmiss if item[0] == move]:
                attacker=line.split(" ",1)[1].split('|')[0]
                recipient=line.split("p1a: ",1)[1].split('|')[0]
                oddsofmiss=round(1-[item[1] for item in movesthatcanmiss if item[0] == move][0]/100,2)
                team2expectedmiss=oddsofmiss
                team1expectedmissagainst=oddsofmiss
                results,attacker=luckiterator(results,attacker,'team2',team2expectedmiss)
                results,recipient=luckiterator(results,recipient,'team1',-team1expectedmissagainst)
        if line.find('|move|p1a: ')>-1 and line.find('[miss]')>-1:
            move=line.split(" ",1)[1].split("|")[1]
            attacker=line.split(" ",1)[1].split('|')[0]
            recipient=line.split("p2a: ",1)[1].split('|')[0]
            team1miss+=1
            team2missagainst+=1
            results,attacker=luckiterator(results,attacker,'team1',-team1miss)
            results,recipient=luckiterator(results,recipient,'team2',team2missagainst)
            results['significantevents'].append([turn,f'{attacker} missed {move} vs {recipient}.'])
        if line.find('|move|p2a: ')>-1 and line.find('[miss]')>-1:
            move=line.split(" ",1)[1].split("|")[1]
            attacker=line.split(" ",1)[1].split('|')[0]
            recipient=line.split("p1a: ",1)[1].split('|')[0]
            team2miss+=1
            team1missagainst+=1
            results,attacker=luckiterator(results,attacker,'team2',-team2miss)
            results,recipient=luckiterator(results,recipient,'team1',team1missagainst)
            results['significantevents'].append([turn,f'{attacker} missed {move} vs {recipient}.'])
    results['team1']['luck']+=team1missagainst-team1miss+team1expectedmiss-team1expectedmissagainst
    results['team2']['luck']+=team2missagainst-team2miss+team2expectedmiss-team2expectedmissagainst
    return results

def critcheck(results,turndata,turn):
    team1expectedcritsfor=0
    team2expectedcritsfor=0
    team1expectedcritsagainst=0
    team2expectedcritsagainst=0
    team1critsfor=0
    team2critsfor=0
    team1critsagainst=0
    team2critsagainst=0
    for line in turndata:
        if line.find("|move|p1a:")>-1 and line.find("|p2a:")>-1:
            move=line.split(" ",1)[1].split("|")[1]
            attacker=line.split(" ",1)[1].split('|')[0]
            recipient=line.split("p2a: ",1)[1].split('|')[0]
            team1expectedcritsfor+=.04167
            team2expectedcritsagainst+=.04167
            results,attacker_=luckiterator(results,attacker,'team1',-team1expectedcritsfor)
            results,recipient_=luckiterator(results,recipient,'team2',team2expectedcritsagainst)
        elif line.find("|move|p2a:")>-1 and line.find("|p1a:")>-1:
            move=line.split(" ",1)[1].split("|")[1]
            attacker=line.split(" ",1)[1].split('|')[0]
            recipient=line.split("p1a: ",1)[1].split('|')[0]
            team2expectedcritsfor+=.04167
            team1expectedcritsagainst+=.04167
            results,attacker_=luckiterator(results,attacker,'team2',-team2expectedcritsfor)
            results,recipient_=luckiterator(results,recipient,'team1',team1expectedcritsagainst)
        elif line.find("|-crit|p1a: ")>-1:
            team2critsfor+=1
            team1critsagainst+=1
            results,attacker_=luckiterator(results,attacker,'team2',team2critsfor)
            results,recipient_=luckiterator(results,recipient,'team1',-team1critsagainst)
            results['significantevents'].append([turn,f'{attacker_} landed a critical hit on {recipient_} with {move}.'])
        elif line.find("|-crit|p2a: ")>-1:
            team1critsfor+=1
            team2critsagainst+=1
            results,attacker_=luckiterator(results,attacker,'team1',team1critsfor)
            results,recipient_=luckiterator(results,recipient,'team2',-team2critsagainst)
            results['significantevents'].append([turn,f'{attacker_} landed a critical hit on {recipient_} with {move}.'])
    results['team1']['luck']+=team1critsfor-team1critsagainst+team1expectedcritsagainst-team1expectedcritsfor
    results['team2']['luck']+=team2critsfor-team2critsagainst+team2expectedcritsagainst-team2expectedcritsfor
    return results

def luckiterator(results,pokemon,team,amount):
    for mon in results[team]['roster']:
        if mon['nickname']==pokemon:
            mon['luck']+=amount
            mon['luck']=round(mon['luck'],2)
            pokemon=mon['pokemon']
    return results,pokemon