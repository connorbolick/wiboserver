from django import template
import datetime
import locale
from decimal import Decimal

register = template.Library()

@register.filter()
def currency(value):
    try:
        return locale.currency(float(value), grouping=True)
    except Exception:
        return "$0.00"

@register.filter()
def percent(value):
    return '{0:.2%}'.format(value)

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''

@register.filter(name='divide')
def divide(val1, val2):
    if val2 == 0:
        return val1
    else:
        return val1/val2

@register.filter(name='add')
def divide(val1, val2):
    return val1 + val2

@register.filter(name='timeformat')
def timeformat(val1):

    if val1 != '':
        val1 = Decimal(val1)
        d = divmod(val1, 86400)
        h = divmod(d[1], 3600)
        m = divmod(h[1], 60)
        s = m[1]

        if d[0] > 0:
            return '%dd, %dh, %dm, %ds' % (d[0],h[0],m[0],s)
        else:
            if h[0] > 0:
                return '%dh, %dm, %ds' % (h[0],m[0],s)
            else:
                if [0] > 0:
                    return '%dm, %ds' % (m[0],s)
                else:
                    return '%ds' % (s)
    else:
        return 'N/A'