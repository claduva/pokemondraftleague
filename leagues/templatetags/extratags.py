import re 
import math

from pokemondatabase.models import *

from django import template
register = template.Library()

@register.filter(name='replace')
def replace(string, arg):
    search=arg.split(",")[0]
    replacement=arg.split(",")[1]
    return string.replace(search, replacement)

@register.filter(name='s2u')
def s2u(string):
    return string.replace(" ", "_")

@register.filter(name='pkmnreplace')
def pkmnreplace(string, arg):
    return string.replace('PKMN', arg)

@register.filter(name='split')
def split(string, arg):
    return string.split(".")[arg]

@register.filter(name='get_replay_string')
def get_replay_string(string):
    string=string.split("/logfiles/")[1].split(".txt")[0]
    return string

@register.filter(name='subtract')
def subtract(num, arg):
    try:
        return num-arg
    except:
        return 0

@register.filter(name='divide')
def divide(int, arg):
    return round(int/arg,2)

@register.filter(name='percentage')
def percentage(int, arg):
    try:
        return round(arg/int*100,2)
    except:
        return 0.00

@register.filter(name='winpercentage')
def winpercentage(win, loss):
    try:
        return str(round(win/(win+loss)*100,2))+"%"
    except:
        return "N/A"
    

@register.filter
def halve(thelist):
    firsthalf=[]
    secondhalf=[]
    i=0
    for item in thelist:
        if i%2==0:
            firsthalf.append(item)
        else:
            secondhalf.append(item)
        i+=1
    return [firsthalf,secondhalf]

@register.filter
def half(thelist,side):
    length=len(thelist)
    half=math.ceil(length/2)
    if side==1:
        qs=thelist[0:half]
    else:
        qs=thelist[half:]
    return qs

@register.filter
def integer(string):
    return int(string)

@register.filter(name='limitquery')
def limitquery(query, arg):
    return query[0:arg]

@register.filter(name='alphabetize')
def alphabetize(query,arg):
    return query.order_by(arg)

@register.filter(name='speed')
def speed(value,arg):
    multiplier=int(arg.split(",")[0])
    lvl=int(arg.split(",")[1])
    neutral=math.floor((((2*value+31+252/4)*lvl)/100+5)*1.1)
    if multiplier==-2:
        resp=math.floor(neutral*1/2)
    elif multiplier==-1:
        resp=math.floor(neutral*2/3)
    elif multiplier==0:
        resp=neutral
    elif multiplier==1:
        resp=math.floor(neutral*3/2)
    elif multiplier==2:
        resp=math.floor(neutral*2)  
    return resp

@register.filter(name='movefilter')
def movefilter(query):
    moves=['Stealth Rock','Spikes','Toxic Spikes','Sticky Web','Defog','Rapid Spin','Court Change','Heal Bell','Aromatherapy','Wish']
    resp=query.filter(moveinfo__name__in=moves)
    return resp

@register.filter(name='sprite')
def sprite(value,arg):
    try:
        poi=all_pokemon.objects.get(pokemon=value)
        if arg=="swsh/ani/standard/PKMN.gif":
            string=poi.sprite.dexaniurl
        elif arg=="swsh/ani/shiny/PKMN.gif":
            string=poi.sprite.dexanishinyurl
        elif arg=="swsh/png/standard/PKMN.png":
            string=poi.sprite.dexurl
        elif arg=="swsh/png/shiny/PKMN.png":
            string=poi.sprite.dexshinyurl
        elif arg=="bw/png/standard/PKMN.png":
            string=poi.sprite.bwurl
        elif arg=="bw/png/shiny/PKMN.png":
            string=poi.sprite.bwshinyurl
        elif arg=="afd/png/standard/PKMN.png":
            string=poi.sprite.afdurl
        elif arg=="afd/png/shiny/PKMN.png":
            string=poi.sprite.afdshinyurl
    except:
        string=""
    return string

@register.filter(name='standings')
def standings(query):
    resp=query.order_by('-wins','losses','-differential','teamname')
    return resp

@register.filter(name='list_standings')
def list_standings(query):
    resp=sorted(query,key=lambda x: x.teamname)
    resp=sorted(resp,key=lambda x: x.differential,reverse=True)
    resp=sorted(resp,key=lambda x: x.losses)
    resp=sorted(resp,key=lambda x: x.wins,reverse=True)
    return resp

@register.filter(name='ordinal')
def ordinal(query):
    if query==1:
        resp="1st"
    elif query==2:
        resp="2nd"
    elif query==3:
        resp="3rd"
    else:
        resp=str(query)+"th"
    return resp