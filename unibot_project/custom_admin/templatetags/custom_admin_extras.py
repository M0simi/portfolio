from django import template

register = template.Library()

@register.filter
def attr(obj, path):
    """يوصل لخاصية متداخلة: attr:'category__name' مثلاً"""
    cur = obj
    for part in path.split('__'):
        cur = getattr(cur, part, None)
        if callable(cur):
            cur = cur()
        if cur is None:
            break
    return cur
