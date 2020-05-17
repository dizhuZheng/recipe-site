from django.template import Library

register = Library()

@register.filter
def get_attr(d, m):
    if hasattr(d.last, m):
        return get_attr(d.last, m)
