import re 
import math

from django import template
register = template.Library()

@register.filter(name='replace')
def replace(string, arg):
    search=arg.split(",")[0]
    replacement=arg.split(",")[1]
    return string.replace(search, replacement)

@register.filter(name='pkmnreplace')
def pkmnreplace(string, arg):
    return string.replace('PKMN', arg)

@register.filter(name='split')
def split(string, arg):
    return string.split(".")[arg]

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
    return round(arg/int*100,2)

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
    moves=['Stealth Rock','Spikes','Toxic Spikes','Sticky Web','Defog','Rapid Spin','Heal Bell','Aromatherapy','Wish']
    resp=query.filter(moveinfo__name__in=moves)
    return resp

@register.filter(name='sprite')
def sprite(value,arg):
    value_=value.replace(":","")
    string="/static/pokemondatabase/sprites/"+arg
    string=string.replace("PKMN",value_)
    return string

@register.filter(name='standings')
def standings(query):
    resp=query.order_by('-wins','losses','-differential','teamname')
    return resp