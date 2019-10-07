def miss_function(line,attacker,target,move,results):
    attacker['luck']+=-1
    target['luck']+=1
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
    ['Thunder Punch', ['status', 'par',target['pokemon'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Fire Punch', ['status', 'brn',target['pokemon'],.1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Zing Zap', ['', 'flinch', .3]], 
    ['Extrasensory', ['', 'flinch', .1]], 
    ['Ice Punch', ['status', 'frz',target['pokemon'], .1]], 
    ['Thunder Shock', ['status', 'par',target['pokemon'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Poison Sting', ['status', 'psn', target['pokemon'], .3]], 
    ['Focus Blast', ['', 'boosts spd: -1 ', .1]], 
    ['Liquidation', ['', 'boosts def: -1 ', .2]], 
    ['Crush Claw', ['', 'boosts def: -1 ', .5]], 
    ['Metal Claw', ['', 'self boosts: atk: 1 ', .1]], 
    ['Acid', ['', 'boosts spd: -1 ', .1]], 
    ['Aurora Beam', ['', 'boosts atk: -1 ', .1]], 
    ['Heart Stamp', ['', 'flinch', .3]], 
    ['Crunch', ['', 'boosts def: -1 ', .2]], 
    ['Water Pulse', ['', 'confusion', .2]], 
    ['Blizzard', ['status', 'frz', target['pokemon'], .1]], 
    ['Paleo Wave', ['', 'boosts atk: -1 ', .2]], 
    ['Freeze-Dry', ['status', 'frz', target['pokemon'], .1]], 
    ['Dizzy Punch', ['', 'confusion', .2]], 
    ['Relic Song', ['status', 'slp', target['pokemon'], .1]], 
    ['Signal Beam', ['', 'confusion', .1]], 
    ['Ancient Power', ['', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', .1]], 
    ['Steamroller', ['', 'flinch', .3]], 
    ['Bubble Beam', ['', 'boosts spe: -1 ', .1]], 
    ['Sludge', ['status', 'psn', target['pokemon'], .3]], 
    ['Play Rough', ['', 'boosts atk: -1 ', .1]], 
    ['Astonish', ['', 'flinch', .3]], 
    ['Energy Ball', ['', 'boosts spd: -1 ', .1]], 
    ['Zen Headbutt', ['', 'flinch', .2]], 
    ['Iron Tail', ['', 'boosts def: -1 ', .3]], 
    ['Shadow Strike', ['', 'boosts def: -1 ', .5]], 
    ['Charge Beam', ['', 'self boosts: spa: 1 ', .7]], 
    ['Secret Power', ['status', 'par', target['pokemon'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Tri Attack', ['status', 'par' or 'frz' or 'brn',target['pokemon'],.2,f"{target['pokemon']} was statused by {attacker['pokemon']} with {move}"]], 
    ['Psychic', ['', 'boosts spd: -1 ', .1]], 
    ['Smog', ['status', 'psn',target['pokemon'],.4]], 
    ['Steel Wing', ['', 'self boosts: def: 1 ', .1]], 
    ['Iron Head', ['', 'flinch', .3]], 
    ['Headbutt', ['', 'flinch', .3]], 
    ['Body Slam', ['status', 'par',target['pokemon'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Bug Buzz', ['', 'boosts spd: -1 ', .1]], 
    ['Seed Flare', ['', 'boosts spd: -2 ', .4]], 
    ['Mist Ball', ['', 'boosts spa: -1 ', .5]], 
    ['Earth Power', ['', 'boosts spd: -1 ', .1]], 
    ['Bolt Strike', ['status', 'par', target['pokemon'], .2,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Bite', ['', 'flinch', .3]], 
    ['Flamethrower', ['status', 'brn',target['pokemon'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Rock Climb', ['', 'confusion', .2]], 
    ['Freeze Shock', ['status', 'par', .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Dark Pulse', ['', 'flinch', .2]], 
    ['Flash Cannon', ['', 'boosts spd: -1 ', .1]], 
    ['Floaty Fall', ['', 'flinch', .3]], 
    ['Poison Fang', ['status', 'tox', target['pokemon'], .5]], 
    ['Sludge Bomb', ['status', 'psn', target['pokemon'], .3]], 
    ['Lick', ['status','par',target['pokemon'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Diamond Storm', ['', 'self boosts: def: 2 ', .5]], 
    ['Shadow Ball', ['', 'boosts spd: -1 ', .2]], 
    ['Cross Poison', ['status', 'psn',target['pokemon'], .1]], 
    ['Sludge Wave', ['status', 'psn',target['pokemon'], .1]], 
    ['Leaf Tornado', ['', 'boosts accuracy: -1 ', .5]], 
    ['Hyper Fang', ['', 'flinch', .1]], 
    ['Muddy Water', ['', 'boosts accuracy: -1 ', .3]], 
    ['Thunder', ['status', 'par',target['pokemon'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Constrict', ['', 'boosts spe: -1 ', .1]], 
    ['Stomp', ['', 'flinch', .3]], 
    ['Poison Tail', ['status', 'psn',target['pokemon'], .1]], 
    ['Bone Club', ['', 'flinch', .1]], 
    ['Fire Blast', ['status', 'brn',target['pokemon'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Mud Bomb', ['', 'boosts accuracy: -1 ', .3]], 
    ['Twineedle', ['status', 'psn',target['pokemon'],.2]], 
    ['Splishy Splash', ['status', 'par',target['pokemon'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Confusion', ['', 'confusion', .1]], 
    ['Steam Eruption', ['status', 'brn',target['pokemon'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Fiery Dance', ['', 'self boosts: spa: 1 ', .5]], 
    ['Night Daze', ['', 'boosts accuracy: -1 ', .4]], 
    ['Flare Blitz', ['status', 'brn',target['pokemon'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Mirror Shot', ['', 'boosts accuracy: -1 ', .3]], 
    ['Sacred Fire', ['status', 'brn',target['pokemon'], .5,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Ice Beam', ['status', 'frz',target['pokemon'], .1]], 
    ['Poison Jab', ['status', 'psn',target['pokemon'], .3]], 
    ['Double Iron Bash', ['', 'flinch', .3]], 
    ['Waterfall', ['', 'flinch', .2]], 
    ['Psybeam', ['', 'confusion', .1]], 
    ['Octazooka', ['', 'boosts accuracy: -1 ', .5]], 
    ['Spark', ['status', 'par',target['pokemon'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Needle Arm', ['', 'flinch', .3]], 
    ['Dragon Breath', ['status', 'par',target['pokemon'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Air Slash', ['', 'flinch', .3]], 
    ['Dragon Rush', ['', 'flinch', .2]], 
    ['Silver Wind', ['', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', .1]], 
    ['Luster Purge', ['', 'boosts spd: -1 ', .5]], 
    ['Snore', ['', 'flinch', .3]], 
    ['Thunderbolt', ['status', 'par',target['pokemon'], .1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Flame Wheel', ['status', 'brn',target['pokemon'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Bounce', ['status', 'par',target['pokemon'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Scald', ['status', 'brn',target['pokemon'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Force Palm', ['status', 'par',target['pokemon'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Hurricane', ['', 'confusion', .3]], 
    ['Ice Burn', ['status', 'brn',target['pokemon'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Gunk Shot', ['status', 'psn',target['pokemon'], .3]], 
    ['Blaze Kick', ['status', 'brn',target['pokemon'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Lava Plume', ['status', 'brn',target['pokemon'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Meteor Mash', ['', 'self boosts: atk: 1 ', .2]], 
    ['Searing Shot', ['status', 'brn',target['pokemon'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Twister', ['', 'flinch', .2]], 
    ['Icicle Crash', ['', 'flinch', .3]], 
    ['Bubble', ['', 'boosts spe: -1 ', .1]], 
    ['Rock Smash', ['', 'boosts def: -1 ', .5]], 
    ['Volt Tackle', ['status', 'par',target['pokemon'], .1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Ember', ['status', 'brn',target['pokemon'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Powder Snow', ['status', 'frz',target['pokemon'], .1]], 
    ['Moonblast', ['', 'boosts spa: -1 ', .3]], 
    ['Rock Slide', ['', 'flinch', .3]], 
    ['Shadow Bone', ['', 'boosts def: -1 ', .2]], 
    ['Heat Wave', ['status', 'brn',target['pokemon'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Discharge', ['status', 'par',target['pokemon'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Ominous Wind', ['', 'self boosts: spa: 1, spd: 1, atk: 1, def: 1, spe: 1 ', .1]], 
    ['Razor Shell', ['', 'boosts def: -1 ', .5]], 
    ['Rolling Kick', ['', 'flinch', .3]], 
    ['Blue Flare', ['status', 'brn',target['pokemon'], .2,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Sky Attack', ['', 'flinch', .3]]])
    move_=moveswithsecondaryeffect[move]
    turndata=list(filter(lambda x: x[1] == line[1] and x[0] > line[0], parsedlogfile))
    for line_ in turndata:
        if line_[2]==move_[0] and line_[3].find(move_[1])>-1 and line_[3].find(move_[2])>-1:
            results['significantevents'].append([line[1],f"LUCK: {move_[4]}"])
            attacker['luck']+=1
            target['luck']+=-1
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
            attacker['luck']+=1
            crittedmon_['luck']+=-1
            move=line_[3].split("|")[1]
            results['significantevents'].append([line[1],f"LUCK: {crittedmon} was crit by {attacker['pokemon']}"])
        elif crittedteam=="p2a" and line_[2]=="move" and line_[3].split(":",1)[0]=="p1a" and line_[3].split("|")[2]==f"{crittedteam}: {crittedmon}":
            attackingteam="p1a"
            attacker=line_[3].split("|",1)[0].split(" ",1)[1]
            attacker=roster_search(attackingteam,attacker,results)
            attacker['luck']+=1
            crittedmon_['luck']+=-1
            move=line_[3].split("|")[1]
            results['significantevents'].append([line[1],f"LUCK: {attacker['pokemon']} landed a crit on {crittedmon} with "])
    return line,parsedlogfile,results
