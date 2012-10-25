# -*- coding: utf-8 -*-
from sz.core.algorithms.tagging import *
from sz.core import venue
import urllib

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

def venue_location_search_service(position, query):
    result = venue.search(position, query)
    return {"places": map(lambda l: {
        "name": l[u'name'].encode('utf8'),
        "address": l[u'location'].get(u'address'),
        "distance": l[u'location'].get(u'distance'),
        "latitude": l[u'location'].get(u'lat'),
        "longitude": l[u'location'].get(u'lng'),
        "venue_id": l[u'id'],
    }, result["venues"])}