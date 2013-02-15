# -*- coding: utf-8 -*-
from django.utils import timezone
from sz.core import lists, queries
from sz.core import gis as gis_core


class ModelCachingService:
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
    def __init__(self, city_service, venue_service, caching_service, categorization_service):
        self.venue_service = venue_service
        self.city_service = city_service
        self.caching_service = caching_service
        self.categorization_service = categorization_service

    def feed(self, **kwargs):
        latitude = kwargs.get('latitude', None)
        longitude = kwargs.get('longitude', None)
        assert latitude and longitude, 'latitude and longitude are required'
        city = self.city_service.get_city_by_position(longitude, latitude)
        kwargs['city_id'] = city['id']
        query = kwargs.pop('query', None)
        kwargs['stems'] = self.categorization_service.detect_stems(query)
        #print u"; ".join(u"(stem: %s, lang: % s)" % stem for stem in kwargs['stems'])
        places = queries.feed(**kwargs)
        messages = queries.messages(places, **kwargs)
        feed = [
            {
                "place": place,
                "distance": gis_core.calculate_distance(longitude, latitude, place.longitude(), place.latitude()),
                "messages": filter(lambda m: m.place.id == place.id, messages),
            }
            for place in places]
        return feed
        #self.venue_service.search({'latitude':latitude, 'longitude': longitude}, **kwargs)
