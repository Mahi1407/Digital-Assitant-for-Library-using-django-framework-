from django import template
import datetime

register = template.Library()

@register.simple_tag
def Overduedays(a, b, c):
    dt = datetime.date(a, b, c)
    now = datetime.datetime.now()
    nowdt = now.date()
    if dt>=nowdt:
        return 0
    else:
        return (nowdt-dt).days

@register.simple_tag
def fine(a, b, c):
    return Overduedays(a, b, c)*2

