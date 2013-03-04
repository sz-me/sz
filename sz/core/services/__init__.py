# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.db.models import Max
from sz import settings
from sz.core import lists, models, queries, gis as gis_core, utils
from sz.core.gis import venue
from sz.core.services import parameters
from sz.core.services.parameters import names as params_names


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

    def __make_result(self, items, count, params):
        return dict(count=count, items=items, params=params)

    def __get_max_id(self):
        return models.Message.objects.aggregate(max_id=Max('id'))["max_id"]

    def __make_place_distance_item(self, place, params):
        latitude, longitude = parameters.get_position_from_dict(params.get_api_params())
        distance = gis_core.calculate_distance(longitude, latitude, place.longitude(), place.latitude())
        item = dict(place=place, distance=distance)
        return item

    def __make_feed_item(self, place, params):
        messages = self.get_place_messages(place, **params.get_api_params())
        item = self.__make_place_distance_item(place, params)
        item['messages'] = messages
        return item

    def get_place_messages(self, place, current_max_id=None, default_limit=settings.DEFAULT_PAGINATE_BY, **kwargs):
        if current_max_id is None:
            current_max_id = self.__get_max_id()
        params = parameters.PlaceMessagesParametersFactory.create(
            kwargs, self.categorization_service, current_max_id, default_limit)
        messages, count = queries.place_messages(place, **params.get_db_params())
        return self.__make_result(messages, count, params.get_api_params())

    def get_news_feed(self, **kwargs):
        current_max_id = self.__get_max_id()
        default_limit = settings.DEFAULT_PAGINATE_BY
        params = parameters.NewsFeedParametersFactory.create(
            kwargs, self.categorization_service, self.city_service, current_max_id, default_limit)
        places, count = queries.places_news_feed(**params.get_db_params())
        kwargs.pop(params_names.LIMIT)
        kwargs.pop(params_names.OFFSET)
        item_params = parameters.PlaceNewsFeedParametersFactory.create(
            kwargs, self.categorization_service, current_max_id, 3)
        feed = self.__make_result(
            [self.__make_feed_item(place, item_params)
             for place in places], count, params.get_api_params())
        return feed

    def get_place_news_feed(self, place, **kwargs):
        current_max_id = self.__get_max_id()
        params = parameters.PlaceNewsFeedParametersFactory.create(
            kwargs, self.categorization_service, current_max_id, 17)
        item = self.__make_feed_item(place, params)
        return item

    def search(self, **kwargs):
        params = parameters.PlaceSearchParametersFactory.create(kwargs, self.city_service)
        places = queries.places(**params.get_db_params())
        return [self.__make_place_distance_item(place, params) for place in places]

    def venue_search(self, **kwargs):
        params = parameters.PlaceSearchParametersFactory.create(kwargs, self.city_service).get_db_params()
        latitude = params.get(params_names.LATITUDE)
        longitude = params.get(params_names.LONGITUDE)
        city_id = params.get(params_names.CITY_ID)
        query = params.get(params_names.QUERY)
        radius = params.get(params_names.RADIUS)
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
