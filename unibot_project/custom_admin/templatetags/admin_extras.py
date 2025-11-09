from django import template

register = template.Library()

@register.filter
def attr(obj, name):
    """Access attribute by string in templates."""
    parts = name.split("__")
    val = obj
    for p in parts:
        val = getattr(val, p, None)
        if val is None:
            return None
    return val
