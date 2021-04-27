from django import template
from random import sample


register = template.Library()

STOP_LIST = [
    'дурак',
]

@register.filter(name='rude')
def clean_text(value):
    for word in value.split():
        if word in STOP_LIST:
            value = value.replace(word,'***')
    return value