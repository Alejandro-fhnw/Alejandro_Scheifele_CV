from django import template

register = template.Library()

@register.filter
def phone_link(value):
    # Beispiel: "0798205475" -> "+41798205475"
    if value.startswith('0'):
        return '+41' + value[1:]
    return value
