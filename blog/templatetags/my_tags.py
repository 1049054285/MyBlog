from django import template

register = template.Library()

@register.filter
def minus(num, minus_num):
    # print(num, '+', plus_num, '=', num + plus_num)
    return int(num) - int(minus_num)

@register.filter
def multi(num, a):
    # print(num, '+', plus_num, '=', num + plus_num)
    return int(num) * int(a)

@register.filter
def get_len(obj_list):
    return len(obj_list)

@register.filter
def reverse_minus(num, minus_num):
    # print(num, '+', plus_num, '=', num + plus_num)
    return int(minus_num) - int(num)

@register.filter
def parse_enter(v):
    ret = []
    for i in v:
        if i == '\r' or i == '\n':
            ret.append("<br>")
        else:
            ret.append(i)
    ret = ''.join(ret)
    return ret

@register.filter
def parseInt(v):
    return int(v)

@register.filter
def print_test(v):
    print(v,type(v))
    return v


# @register.filter
# def get_value_by_key(dic, key):
#     return dic.get(key)
#
#
#

#
