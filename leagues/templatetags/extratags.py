import re 

from django import template
register = template.Library()

@register.filter(name='replace')
def replace(string, arg):
    search=arg.split(",")[0]
    replacement=arg.split(",")[1]
    return string.replace(search, replacement)