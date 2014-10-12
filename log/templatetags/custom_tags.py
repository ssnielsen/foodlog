from django import template
import sys

register = template.Library()

@register.filter(name='getkey')
def getkey(value, arg):
    return value[arg]

@register.assignment_tag
def get_twitter_bootstrap_alert_msg_css_name(tags):
    return 'danger' if tags == 'error' else tags