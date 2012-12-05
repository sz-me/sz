# -*- coding: utf-8 -*-
from django.core import paginator as django_paginator
from sz.core.algorithms.tagging import *
from sz.core import venue
from sz.core import models

def paginated_content(queryset, page=None, paginate_by=5):
    paginator = django_paginator.Paginator(queryset, paginate_by)
    try:
        messages = paginator.page(page)
    except django_paginator.PageNotAnInteger:
        messages = paginator.page(1)
    except django_paginator.EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return messages

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

def venue_place_service(position, query = None, radius = None):
    result = venue.search(position, query, radius)
    place_and_distance_list = map(
        lambda l: {
            'place': models.Place(
                id = l[u'id'],
                name = l[u'name'].encode('utf8'),
                contact = l.get(u'contact'),
                address = u"%s" % l[u'location'].get(u'address'),
                crossStreet = u"%s" % l[u'location'].get(u'crossStreet'),
                latitude = l[u'location'].get(u'lat'),
                longitude = l[u'location'].get(u'lng')),
            'distance': l[u'location'].get(u'distance'),
        },
        result["venues"])
    return place_and_distance_list

from sz.core import geonames
def geonames_city_service(position, query):

    response = lambda g : {
        "name": g['name'],
        "region": g['adminName1'],
        "country": g['countryName'],
        "country_code": g['countryCode'],
        "latitude": g['lat'],
        "longitude": g['lng'],
        "geoname_id": g['geonameId'],
        "international_name": g['toponymName']
    }

    if query:
        request = geonames.search(query)
        return [ response(g) for g in request['geonames']]
    else:
        request = geonames.nearby(position)
        return [ response(g) for g in request['geonames']]

