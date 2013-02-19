# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.db.models import Max
from sz.core import lists, models, queries, gis as gis_core, utils
from sz.core.gis import venue


class ModelCachingManager:
    stored = []
    cached = []
    for_insert = []
    for_update = []

    def __init__(self, data, date, delta):
        assert data, 'data is required'
        if len(data) > 0:
            assert date, 'date is required'
            assert delta, 'delta is required'
            data = set(data)
            model_class = type(lists.first(data))
            assert lists.all(lambda e: type(e) == model_class, data), \
                'data contain items of different types'
            self.stored = model_class.objects.filter(pk__in=[e.id for e in data])
            db = map(lambda e: dict(pk=e.id, date=date(e)), self.stored)
            non_cached_entities = set(filter(lambda e: e.pk not in [x['pk'] for x in db], data))
            self.cached = data - non_cached_entities
            last_update_date = lambda e: \
                filter(lambda x: x['pk'] == e.pk, db)[0]['date']
            expired_places = filter(lambda e: timezone.now() - last_update_date(e) > delta, self.cached)

            self.for_insert = non_cached_entities
            self.for_update = expired_places

    def save(self):
        map(lambda e: e.save(force_insert=True), self.for_insert)
        map(lambda e: e.save(force_update=True), self.for_update)


class PlaceService:
    def __init__(self, city_service, venue_service, categorization_service):
        self.venue_service = venue_service
        self.city_service = city_service
        self.categorization_service = categorization_service

    def _get_city(self, **kwargs):
        latitude, longitude = utils.get_position_from_kwargs(**kwargs)
        city = self.city_service.get_city_by_position(longitude, latitude)
        return city

    def _make_result(self, items, count, **kwargs):
        latitude, longitude = utils.get_position_from_kwargs(**kwargs)
        limit, offset, max_id = utils.get_paging_args(**kwargs)
        query = kwargs.get('query', None)
        category = kwargs.get('category', None)
        return dict(latitude=latitude, longitude=longitude, query=query, category=category, max_id=max_id, limit=limit,
                    offset=offset, count=count, items=items)

    def _place_messages_first(self, place, **kwargs):
        kwargs.pop('limit')
        kwargs.pop('offset')
        return self._place_messages(place, **kwargs)

    def _place_messages(self, place, **kwargs):
        messages, count = queries.place_messages(place, **kwargs)
        return self._make_result(messages, count, **kwargs)

    def feed(self, **kwargs):
        latitude, longitude = utils.get_position_from_kwargs(**kwargs)
        city = self._get_city(**kwargs)
        kwargs['city_id'] = city['id']
        query = kwargs.get('query', None)
        kwargs['stems'] = self.categorization_service.detect_stems(query)
        #print u"; ".join(u"(stem: %s, lang: % s)" % stem for stem in kwargs['stems'])
        max_id = kwargs.get("max_id", None)
        if max_id is None:
            max_id = models.Message.objects.aggregate(max_id=Max('id'))["max_id"]
            kwargs['max_id'] = max_id
        places, count = queries.feed(**kwargs)
        feed = self._make_result(
            [ dict(
                place=place,
                distance=gis_core.calculate_distance(longitude, latitude, place.longitude(), place.latitude()),
                messages=self._place_messages_first(place, **kwargs.copy())
            ) for place in places], count, **kwargs)

        return feed

    def search(self, **kwargs):
        latitude, longitude = utils.get_position_from_kwargs(**kwargs)
        city = self._get_city(**kwargs)
        query = kwargs.get('query', None)
        radius = kwargs.get('radius', None)
        result = venue.search({'latitude': latitude, 'longitude': longitude}, query, radius)
        place_and_distance_list = \
            map(lambda l:
                dict(place=models.Place(
                    id=l[u'id'],
                    name=l[u'name'],
                    contact=l.get(u'contact'),
                    address=l[u'location'].get(u'address') and (u"%s" % l[u'location'].get(u'address')) or None,
                    crossStreet=l[u'location'].get(u'crossStreet') and (u"%s" % l[u'location'].get(u'crossStreet'))
                    or None,
                    position=gis_core.ll_to_point(l[u'location'].get(u'lng'), l[u'location'].get(u'lat')),
                    city_id=None,
                    foursquare_icon_suffix=utils.safe_get(l, lambda el: el[u'categories'][0][u'icon'][u'suffix']),
                    foursquare_icon_prefix=utils.safe_get(l, lambda el: el[u'categories'][0][u'icon'][u'prefix']), ),
                    distance=l[u'location'].get(u'distance')),
                result["venues"])
        if len(place_and_distance_list) > 0:
            caching_manager = ModelCachingManager(
                [item['place'] for item in place_and_distance_list],
                lambda e: e.date, datetime.timedelta(seconds=60 * 60 * 24 * 3))
            city_id = city['id']
            if len(caching_manager.for_insert) > 0:
                for e in caching_manager.for_insert:
                    e.city_id = city_id
            if len(caching_manager.cached) > 0:
                for e in caching_manager.cached:
                    stored_city = lists.first_match(lambda x: x.id == e.id, caching_manager.stored)
                    e.city_id = stored_city.city_id
            caching_manager.save()
        return place_and_distance_list
        #self.venue_service.search({'latitude':latitude, 'longitude': longitude}, **kwargs)
