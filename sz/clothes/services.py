# -*- coding: utf-8 -*-
import re
#from sz.core import spellcorrector
from sz.core.algorithms import lists
from sz.core.algorithms.tagging import *

def tags2dict(tags):
    d = dict((tag.name, [p.value for p in tag.pattern_set.all()]) for tag in tags)
    return d

def tagging_service(message, tags, algorithm):
    tags_dict = tags2dict(tags)
    return algorithm(message, tags_dict)
    
def regexp_tagging_service(message, tags):
    algorithm = lambda m, t: regexp_tagging_algorithm(m, t)
    return tagging_service(message, tags, algorithm)

def spellcorrector_tagging_service(message, tags):
    algorithm = lambda m, t: spellcorrector_tagging_algorithm(m, t)
    return tagging_service(message, tags, algorithm)