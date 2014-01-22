from django import template
import sys

register = template.Library()

@register.filter(name='getkey')
def getkey(value, arg):
    return value[arg]