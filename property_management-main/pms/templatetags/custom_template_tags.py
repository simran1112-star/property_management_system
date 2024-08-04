from django import template
from word2number import w2n

register = template.Library()

@register.filter
def number_value(value):
    try:
        value = w2n.word_to_num(value)
        return value
    except:
        value = value.split('_')
        return value[-1]+"+"


@register.filter
def replace_underscores(string):
    return string.replace('_', ' ')
