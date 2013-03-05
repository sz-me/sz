# -*- coding: utf-8 -*-
import datetime
from django.db import models as dj_models
from django.db.models import Q
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.utils import timezone
from sz.core import models
from sz.core.services.parameters import names as params_names


def places(**kwargs):
    latitude = kwargs.get(params_names.LATITUDE)
    longitude = kwargs.get(params_names.LONGITUDE)
    limit = 15 #kwargs.get(params_names.LIMIT)
    query = kwargs.get(params_names.QUERY)
    current_position = fromstr("POINT(%s %s)" % (longitude, latitude))
    radius = kwargs.get(params_names.RADIUS)
    filtered_places = models.Place.objects.annotate(messages_count=dj_models.Count('message__id'))\
        .order_by('-messages_count')
    if query:
        filtered_places = filtered_places.filter(name__icontains=query)
    if radius == 0 or radius is None:
        # TODO: определять город по координатам
        city_id = kwargs.get(params_names.CITY_ID)
        assert city_id, 'city_id is required'
        filtered_places = filtered_places.filter(city_id=city_id)
    else:
        distance_kwargs = {'m': '%i' % radius}
        filtered_places = filtered_places.filter(position__distance_lte=(current_position, D(**distance_kwargs)))
    filtered_places = filtered_places.distance(current_position).order_by('distance')[:limit]
    return filtered_places


def places_news_feed(**kwargs):
    """
    Возвращает ленту последний событий в городе или в близлежащих местах,
    если задан аргумент :radius:, то рассматриваются
    места в радиусе данного значения (в метрах).
    """
    latitude = kwargs.get(params_names.LATITUDE)
    longitude = kwargs.get(params_names.LONGITUDE)
    limit = kwargs.get(params_names.LIMIT)
    offset = kwargs.get(params_names.OFFSET)
    max_id = kwargs.get(params_names.MAX_ID)
    stems = kwargs.get(params_names.STEMS)
    category = kwargs.get(params_names.CATEGORY)
    current_position = fromstr("POINT(%s %s)" % (longitude, latitude))
    radius = kwargs.get(params_names.RADIUS)
    filtered_places = models.Place.objects.annotate(last_message=dj_models.Max('message__id'))\
        .filter(last_message__isnull=False)
    if max_id is not None:
        filtered_places = filtered_places.filter(message__id__lte=max_id)
    if radius == 0 or radius is None:
        # TODO: определять город по координатам
        city_id = kwargs.get(params_names.CITY_ID)
        assert city_id, 'city_id is required'
        filtered_places = filtered_places.filter(city_id=city_id)
    else:
        distance_kwargs = {'m': '%i' % radius}
        filtered_places = filtered_places.filter(position__distance_lte=(current_position, D(**distance_kwargs)))\
            .distance(current_position).order_by('distance')
    if len(stems) > 0:
        filtered_places = filtered_places.filter(message__stems__stem__in=[stem[0] for stem in stems])
    if category is not None:
        filtered_places = filtered_places.filter(message__categories__in=[category,])
    count = filtered_places.aggregate(count=dj_models.Count('id'))['count']
    query = filtered_places.order_by('-last_message')[offset:offset + limit]
    return query, count


def messages(places, **kwargs):
    # getting params
    limit = kwargs.get(params_names.LIMIT)
    offset = kwargs.get(params_names.OFFSET)
    max_id = kwargs.get(params_names.MAX_ID)
    stems = kwargs.get(params_names.STEMS)
    category = kwargs.get(params_names.CATEGORY)
    # creating the query
    filtered_messages = models.Message.objects.filter(place__pk__in=[p.pk for p in places])
    if max_id is not None:
        filtered_messages = filtered_messages.filter(id__lte=max_id)
    if len(stems) > 0:
        filtered_messages = filtered_messages.filter(stems__stem__in=[stem[0] for stem in stems])
    if category is not None:
        filtered_messages = filtered_messages.filter(categories__in=[category,])
    query = filtered_messages.order_by('-date')[offset:offset + limit]
    return query


def place_messages(place, **kwargs):
    # getting params
    limit = kwargs.get(params_names.LIMIT)
    offset = kwargs.get(params_names.OFFSET)
    max_id = kwargs.get(params_names.MAX_ID)
    stems = kwargs.get(params_names.STEMS)
    category = kwargs.get(params_names.CATEGORY)
    # creating the query
    filtered_messages = models.Message.objects.filter(place__pk=place.pk)
    if max_id is not None:
        filtered_messages = filtered_messages.filter(id__lte=max_id)
    if len(stems) > 0:
        filtered_messages = filtered_messages.filter(stems__stem__in=[stem[0] for stem in stems])
    if category is not None:
        filtered_messages = filtered_messages.filter(categories__in=[category, ])
    filtered_messages = filtered_messages.distinct()
    count = filtered_messages.aggregate(count=dj_models.Count('id'))['count']
    query = filtered_messages.order_by('-date')[offset:offset + limit]
    return query, count


def categories(place):
    last_day = timezone.now() - datetime.timedelta(days=56)
    query = models.Category.objects\
    .filter(thing__message__place_id=place.id, thing__message__date__gte=last_day)\
    .values('name').annotate(
        count=dj_models.Count('thing__message'),
        last=dj_models.Max('thing__message__date'))\
    .order_by('-count', '-last')
    return query