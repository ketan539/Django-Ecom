from django import template

register = template.Library()

@register.filter
def add_commas(value):
    """
    Given an integer or a string representation of an integer,
    add commas to the thousands places and return the result.
    """
    try:
        value = int(value)
    except ValueError:
        return value

    orig = str(value)
    new = ''
    for i, c in enumerate(reversed(orig)):
        if i and (i % 3) == 0:
            new += ','
        new += c
    return ''.join(reversed(new))
