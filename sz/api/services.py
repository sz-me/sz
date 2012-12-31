# -*- coding: utf-8 -*-
from django.core import paginator as django_paginator
from sz import settings
from sz.core import models, utils, gis
from sz.core.gis import geonames, venue
from sz.core.morphology.tagging import *

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


def geonames_city_service(position, query=None):

    response = lambda g : {
        "id": g['geonameId'],
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



def venue_place_service(position, query = None, distance = None):
    if not(distance is None):
        distance = utils.safe_cast(distance, int, settings.DEFAULT_DISTANCE)
    result = venue.search(position, query, distance)
    place_and_distance_list = map(
        lambda l: {
            'place': models.Place(
                id = l[u'id'],
                name = l[u'name'],
                contact = l.get(u'contact'),
                address = l[u'location'].get(u'address')
                    and (u"%s" % l[u'location'].get(u'address')) or None,
                crossStreet = l[u'location'].get(u'crossStreet')
                    and (u"%s" % l[u'location'].get(u'crossStreet')) or None,
                position = gis.ll_to_point(l[u'location'].get(u'lng'), l[u'location'].get(u'lat')),
                city_id = None,
                foursquare_icon_suffix = utils.safe_get(l, lambda el: el[u'categories'][0][u'icon'][u'name']),
                foursquare_icon_prefix = utils.safe_get(l, lambda el: el[u'categories'][0][u'icon'][u'prefix']),

            ),
            'distance': l[u'location'].get(u'distance'),
        },
        result["venues"])
    return place_and_distance_list

