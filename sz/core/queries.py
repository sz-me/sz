# -*- coding: utf-8 -*-
import datetime
from django.db import models as dj_models
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.utils import timezone
from sz.core import models, utils
from sz import settings

DEFAULT_DISTANCE = settings.DEFAULT_DISTANCE
# TODO: вынести в sz.settings
DEFAULT_PAGINATE_BY = 7


def feed(**kwargs):
    """
    Возвращает ленту последний событий в городе или в близлежащих местах,
    если задан параметр nearby. Если nearby задан числом, то рассматриваются
    места в радиусе данного значения (в метрах).
    """
    latitude = kwargs.pop('latitude', None)
    longitude = kwargs.pop('longitude', None)
    assert latitude and longitude, 'latitude and longitude are required'
    current_position = fromstr("POINT(%s %s)" % (longitude, latitude))
    paginate_by = kwargs.get('paginate_by', DEFAULT_PAGINATE_BY)
    stems = kwargs.get('stems', [])
    nearby = kwargs.get('nearby', None)
    category = kwargs.get('category', None)

    filtered_places = models.Place.objects.annotate(last_message=dj_models.Max('message__id'))\
        .filter(last_message__isnull=False)
    if nearby is None:
        # TODO: определять город по координатам
        city_id = kwargs.pop('city_id', None)
        assert city_id, 'city_id is required'
        filtered_places = filtered_places.filter(city_id=city_id)
    else:
        distance = utils.safe_cast(nearby, int, DEFAULT_DISTANCE)
        distance_kwargs = {'m':'%i' % distance}
        filtered_places = filtered_places.filter(position__distance_lte=(current_position, D(**distance_kwargs)))\
            .distance(current_position).order_by('distance')
    if len(stems) > 0:
        filtered_places = filtered_places.filter(message__stems__stem__in=[stem[0] for stem in stems])
    if category is not None:
        filtered_places = filtered_places.filter(message__categories__in=[category,])
    query = filtered_places.order_by('-last_message')[:paginate_by]
    return query


def messages(places, **kwargs):
    paginate_by = kwargs.get('paginate_by', DEFAULT_PAGINATE_BY)
    stems = kwargs.get('stems', [])
    category = kwargs.get('category', None)
    filtered_messages = models.Message.objects.filter(place__pk__in=[p.pk for p in places])
    if len(stems) > 0:
        filtered_messages = filtered_messages.filter(stems__stem__in=[stem[0] for stem in stems])
    if category is not None:
        filtered_messages = filtered_messages.filter(categories__in=[category,])
    query = filtered_messages.order_by('-date')[:paginate_by]
    return query


def categories(place):
    last_day = timezone.now() - datetime.timedelta(days=56)
    query = models.Category.objects\
    .filter(thing__message__place_id=place.id, thing__message__date__gte=last_day)\
    .values('name').annotate(
        count=dj_models.Count('thing__message'),
        last=dj_models.Max('thing__message__date'))\
    .order_by('-count', '-last')
    return query