def miss_function(line,attacker,target,move,results):
    attacker['luck']+=-100
    target['luck']+=100
    results['significantevents'].append([line[1],f"LUCK: {attacker['pokemon']} missed {move} against {target['pokemon']}"])
    return results

def roster_search(team,pokemon,results):
    if team=="p1a":
        team="team1"
    elif team=="p2a":
        team="team2"
    for mon in results[team]['roster']:
        if mon['nickname']==pokemon:
            pokemon=mon
    return pokemon

def secondary_check(attacker,target,move,line,results,parsedlogfile):
    moveswithsecondaryeffect=dict([
    ['Thunder Punch', ['status', 'par',target['nickname'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Fire Punch', ['status', 'brn',target['nickname'],.1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Fire Fang', ['status', 'brn',target['nickname'],.1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Zing Zap', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Extrasensory', ['cant', 'flinch',target['nickname'], .1,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Ice Punch', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Ice Fang', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Thunder Fang', ['status', 'par',target['nickname'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Thunder Shock', ['status', 'par',target['nickname'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Poison Sting', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Focus Blast', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Liquidation', ['unboost', 'def|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Crush Claw', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Metal Claw', ['boost', 'atk|1 ',attacker['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Acid', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Aurora Beam', ['unboost', 'atk|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Heart Stamp', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Crunch', ['unboost', 'def|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Water Pulse', ['start', 'confusion',target['nickname'], .2,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Blizzard', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Paleo Wave', ['unboost', 'atk|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Freeze-Dry', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Dizzy Punch', ['start', 'confusion',target['nickname'], .2,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Relic Song', ['status', 'slp',target['nickname'], .1,f"{target['pokemon']} was put to sleep by {attacker['pokemon']} with {move}"]], 
    ['Signal Beam', ['start', 'confusion',target['nickname'], .1,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Ancient Power', ['boost', 'atk|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Steamroller', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Bubble Beam', ['unboost', 'spe|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Sludge', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Play Rough', ['unboost', 'atk|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Astonish', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Energy Ball', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Zen Headbutt', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Iron Tail', ['unboost', 'def|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Shadow Strike', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Charge Beam', ['boost', 'spa|1',target['nickname'], .7,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Secret Power', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Tri Attack', ['status', '',target['nickname'],.2,f"{target['pokemon']} was statused by {attacker['pokemon']} with {move}"]], 
    ['Psychic', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Smog', ['status', 'psn',target['nickname'],.4,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Steel Wing', ['boost', 'def|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Iron Head', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Headbutt', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Body Slam', ['status', 'par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Bug Buzz', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Seed Flare', ['unboost', 'spd|2',target['nickname'], .4,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Mist Ball', ['unboost', 'spa|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Earth Power', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Bolt Strike', ['status', 'par',target['nickname'], .2,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Bite', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Flamethrower', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Rock Climb', ['start', 'confusion',target['nickname'], .2,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Freeze Shock', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Dark Pulse', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Flash Cannon', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Floaty Fall', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Poison Fang', ['status', 'tox',target['nickname'], .5,f"{target['pokemon']} was toxiced by {attacker['pokemon']} with {move}"]], 
    ['Sludge Bomb', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Lick', ['status','par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Diamond Storm', ['boost', 'def|2',target['nickname'], .5,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Shadow Ball', ['unboost', 'spd|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Cross Poison', ['status', 'psn',target['nickname'], .1,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Sludge Wave', ['status', 'psn',target['nickname'], .1,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Leaf Tornado', ['unboost', 'accuracy|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Hyper Fang', ['cant', 'flinch',target['nickname'], .1,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Muddy Water', ['unboost', 'accuracy|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Thunder', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Constrict', ['unboost', 'spe|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Stomp', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Poison Tail', ['status', 'psn',target['nickname'], .1,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Bone Club', ['cant', 'flinch',target['nickname'], .1,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Fire Blast', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Mud Bomb', ['unboost', 'accuracy|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Twineedle', ['status', 'psn',target['nickname'],.2,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Splishy Splash', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Confusion', ['start', 'confusion',target['nickname'], .1,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Steam Eruption', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Fiery Dance', ['boost', 'spa|1',target['nickname'], .5,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Night Daze', ['unboost', 'accuracy|1',target['nickname'], .4,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Flare Blitz', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Mirror Shot', ['unboost', 'accuracy|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Sacred Fire', ['status', 'brn',target['nickname'], .5,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Ice Beam', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Poison Jab', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Double Iron Bash', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Waterfall', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Psybeam', ['start', 'confusion',target['nickname'], .1,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Octazooka', ['unboost', 'accuracy|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Spark', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Needle Arm', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Dragon Breath', ['status', 'par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Air Slash', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Dragon Rush', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Silver Wind', ['boost', 'atk|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Luster Purge', ['unboost', 'spd|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Snore', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Thunderbolt', ['status', 'par',target['nickname'], .1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Flame Wheel', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Bounce', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Scald', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Force Palm', ['status', 'par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Hurricane', ['start', 'confusion',target['nickname'], .3,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Ice Burn', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Gunk Shot', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Blaze Kick', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Lava Plume', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Meteor Mash', ['boost', 'atk|1',target['nickname'], .2,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Searing Shot', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Twister', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Icicle Crash', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Bubble', ['unboost', 'spe|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Rock Smash', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Volt Tackle', ['status', 'par',target['nickname'], .1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Ember', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Powder Snow', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Moonblast', ['unboost', 'spa|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Rock Slide', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Shadow Bone', ['unboost', 'def|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Heat Wave', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Discharge', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Ominous Wind', ['boost', 'atk|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Razor Shell', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Rolling Kick', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Blue Flare', ['status', 'brn',target['nickname'], .2,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Sky Attack', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]]])
    move_=moveswithsecondaryeffect[move]
    turndata=list(filter(lambda x: x[1] == line[1] and x[0] > line[0], parsedlogfile))
    for line_ in turndata:
        if move=="Tri Attack":
            if line_[2]==move_[0] and line_[3].find(move_[2])>-1:
                status=line_[3].split("|")[1]
                if status in ['brn','par','frz']:
                    results['significantevents'].append([line[1],f"LUCK: {move_[4]}"])
                    attacker['luck']+=100
                    target['luck']+=-100
                    target[status]=attacker['nickname']   
                    break
        elif line_[2]==move_[0] and line_[3].find(move_[1])>-1 and line_[3].find(move_[2])>-1:
            results['significantevents'].append([line[1],f"LUCK: {move_[4]}"])
            attacker['luck']+=100
            target['luck']+=-100
            if move_[0]=="status" or move_[0]=="start":
                target[move_[1]]=attacker['nickname']
    return results

def crit_function(line,parsedlogfile,results):
    crittedteam=line[3].split(":",1)[0]
    crittedmon=line[3].split(" ",1)[1]
    crittedmon_=roster_search(crittedteam,crittedmon,results)
    turndata=list(filter(lambda x: x[1] == line[1] and x[0] < line[0], parsedlogfile))
    turndata=turndata[::-1]
    for line_ in turndata:
        if crittedteam=="p1a" and line_[2]=="move" and line_[3].split(":",1)[0]=="p2a" and line_[3].split("|")[2]==f"{crittedteam}: {crittedmon}":
            attackingteam="p2a"
            attacker=line_[3].split("|",1)[0].split(" ",1)[1]
            attacker=roster_search(attackingteam,attacker,results)
            attacker['luck']+=100
            crittedmon_['luck']+=-100
            move=line_[3].split("|")[1]
            results['significantevents'].append([line[1],f"LUCK: {attacker['pokemon']} landed a crit on {crittedmon_['pokemon']} with {move}"])
        elif crittedteam=="p2a" and line_[2]=="move" and line_[3].split(":",1)[0]=="p1a" and line_[3].split("|")[2]==f"{crittedteam}: {crittedmon}":
            attackingteam="p1a"
            attacker=line_[3].split("|",1)[0].split(" ",1)[1]
            attacker=roster_search(attackingteam,attacker,results)
            attacker['luck']+=100
            crittedmon_['luck']+=-100
            move=line_[3].split("|")[1]
            results['significantevents'].append([line[1],f"LUCK: {attacker['pokemon']} landed a crit on {crittedmon_['pokemon']} with {move}"])
    return line,parsedlogfile,results
