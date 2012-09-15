# -*- coding: utf-8 -*-
import re
from sz.core import spellcorrector
def list_debug_info(field, data, msg=''):
    return reduce(
        lambda acc, item: acc + ' ' + field(item), 
        data, msg)

def regexp_tags(message, patterns):
    re_starts_of = lambda pattern: ur'.*\s%s|^%s' % (pattern, pattern)
    """
    print u'Сообщение: ' + message.lower()
    print list_debug_info(
        lambda pattern: u'{#%s - %s}' % (pattern.tag.name, re_starts_of(pattern.value)), 
        patterns, u'Шаблоны:')
    """    
    is_match = lambda pattern: re.match(
        re_starts_of(pattern.value), 
        message.lower(), re.I|re.U)
    matched = filter(is_match, patterns)
    print list_debug_info(lambda pattern: pattern.tag.name, matched, u'Совпадения:')
    tags = map(lambda pattern: pattern.tag, matched)
    return list(set(map(lambda x: x.name, tags)))
    
def spellcorrector_tags(message, patterns):
    corrector = spellcorrector.Corrector(map(lambda pattern: pattern.value, patterns))
    words = spellcorrector.words(message)
    values = filter(lambda w: w, map(lambda w: corrector.correct(w), words))
    tag_names = map(lambda pattern: pattern.tag.name, filter(lambda pattern: pattern.value in values, patterns))
    return list(set(tag_names))