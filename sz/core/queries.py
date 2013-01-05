# -*- coding: utf-8 -*-
import datetime
import functools
from django.db import models as dj_models
from django.db.models import Q
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.utils import timezone
from sz.core import models, utils
from sz import settings

DEFAULT_DISTANCE = settings.DEFAULT_DISTANCE
# TODO: вынести в sz.settings
DEFAULT_PAGINATE_BY = 7

def messages_Q(things, stems):
    messages_with_condition = Q()
    if things:
        messages_with_things = Q(things__in=things)
        messages_with_condition = messages_with_condition & messages_with_things
    if stems:
        messages_with_stems = functools.reduce(lambda f, s: f | Q(text__icontains=s), stems, Q())
        messages_with_condition = messages_with_condition & messages_with_stems
    return messages_with_condition

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
    things = kwargs.pop('things', None)
    stems = kwargs.pop('stems', None)
    filtered_places = models.Place.objects\
        .filter(message__in = models.Message.objects.filter(messages_Q(things, stems)))
    if nearby is None:
        # TODO: определять город по координатам
        city_id = kwargs.pop('city_id', None)
        assert city_id, 'city_id is required'
        filtered_places = filtered_places.filter(city_id=city_id)
    else:
        distance = utils.safe_cast(nearby, int, DEFAULT_DISTANCE)
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

def categories(place):
    last_day = timezone.now() - datetime.timedelta(days=56)
    query = models.Category.objects\
    .filter(thing__message__place_id=place.id, thing__message__date__gte=last_day)\
    .values('name').annotate(
        count = dj_models.Count('thing__message'),
        last = dj_models.Max('thing__message__date'))\
    .order_by('-count', '-last')
    return query