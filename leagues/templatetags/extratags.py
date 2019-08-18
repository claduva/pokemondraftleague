import re 

from django import template
register = template.Library()

@register.filter(name='replace')
def replace(string, arg):
    search=arg.split(",")[0]
    replacement=arg.split(",")[1]
    return string.replace(search, replacement)

@register.filter(name='split')
def split(string, arg):
    return string.split(".")[arg]

@register.filter(name='subtract')
def subtract(int, arg):
    return int-arg

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