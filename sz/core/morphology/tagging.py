# -*- coding: utf-8 -*- 
from sz.core import lists, morphology
from sz.core.morphology import spellcorrector
import re
import functools

def regexp_tagging_algorithm(message, tags):
    re_starts_of = lambda pattern: ur'.*\s%s|^%s' % (pattern, pattern)
    tag_patterns = lambda (k, v): map( 
        lambda value: re_starts_of(value), 
        [k] + v
    )
    is_match = lambda pattern: re.match(pattern, message, re.I|re.U)
    is_tag_matched = lambda tag: lists.any(is_match, tag_patterns(tag))
    matched_tags = filter(is_tag_matched, tags.items())
    tag_names = list(set(map(lambda x: x[0], matched_tags)))
    return tag_names

def spellcorrector_tagging_algorithm(message, tags):
    dict = functools.reduce(
        lambda acc, item: acc + item,
        [[tag] + patterns for (tag, patterns) in tags.items()],
        [])
    corrector = spellcorrector.Corrector(dict)
    words = morphology.extract_words(message)
    values = set(filter(lambda c: c, map(lambda w: corrector.correct(w), words)))
    tag_names = map(
        lambda (k, v): k,
        filter(lambda(k, v): set([k] + v) & values, tags.items()))
    return list(set(tag_names))
    