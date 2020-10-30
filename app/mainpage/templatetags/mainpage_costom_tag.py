from django import template
register = template.Library()

@register.filter
def convert_time(t):
    try:
        h = str(t//60)
        m = str(t%60)
        if len(h) == 1 :
            h = '0' + h
        if len(m) == 1 :
            m = '0' + m
        return h + ':' + m
    except:
        return ''