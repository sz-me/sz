# -*- coding: utf-8 -*-
import exceptions
from django.db import models as dj_models
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from sz.core import models, utilities
from sz import settings

DEFAULT_DISTANCE = settings.DEFAULT_DISTANCE
# TODO: вынести в sz.settings
DEFAULT_PAGINATE_BY = 7

def feed(**kwargs):
    '''
    Возвращает ленту последний событий в городе или в близлежащих местах,
    если задан параметр nearby. Если nearby задан числом, то рассматриваются
    места в радиусе данного значения (в метрах).
    '''
    latitude = kwargs.pop('latitude', None)
    longitude = kwargs.pop('longitude', None)
    assert latitude and longitude, 'latitude and longitude are required'
    current_position = fromstr("POINT(%s %s)" % (longitude, latitude))
    paginate_by = kwargs.pop('paginate_by', DEFAULT_PAGINATE_BY)
    place = kwargs.pop('place', None)
    nearby = kwargs.pop('nearby', None)

    filtered_places = models.Place.objects.exclude(message__id__isnull=True)

    if nearby is None:
        # TODO: определять город по координатам
        city_id = kwargs.pop('city_id', None)
        assert city_id, 'city_id is required'
        filtered_places = filtered_places.filter(city_id=city_id)
    else:
        distance = utilities.safe_cast(nearby, int, DEFAULT_DISTANCE)
        distance_kwargs = {'m':'%i' % distance}
        filtered_places = filtered_places\
        .filter(position__distance_lte=(current_position, D(**distance_kwargs) ))\
        .distance(current_position).order_by('distance')

    if place:
        filtered_places = filtered_places.filter(name__icontains=place)

    query = filtered_places\
            .annotate(last_message=dj_models.Max('message__id'))\
            .order_by('-last_message')[:paginate_by]

    return query
