from django import template

register = template.Library()

@register.filter()
def exclude_first(dict):
    first_key = list(dict)[0]
    del dict[first_key]
    return dict

@register.filter()
def only_first(dict):
    first_key = list(dict)[0]
    return first_key