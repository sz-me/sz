import functools
def debug_info(field, list, msg=''):
    return functools.reduce(lambda acc, item: acc + '\n ' + field(item), list, msg)
def any(condition, list):
    return functools.reduce(lambda acc, item: acc or item, map(condition, list), 0)