import functools
def debug_info(field, list, msg=''):
    return functools.reduce(lambda acc, item: acc + '\n ' + field(item), list, msg)
def any(condition, list):
    return functools.reduce(lambda acc, item: acc or item, map(condition, list), 0)
def all(condition, list):
    return functools.reduce(lambda acc, item: acc and item, map(condition, list), 1)
def first(list):
    return functools.reduce(lambda first, second: first, list)
def last(list):
    return functools.reduce(lambda first, second: second, list)
def first_match(condition, list):
    for x in list:
        if condition(x):
            return x
    return None
def last_match(condition, list):
    return functools.reduce(lambda first, second: condition(second) and second or first, list, None)