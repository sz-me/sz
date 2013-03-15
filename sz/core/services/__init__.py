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


class FeedService:
    def _make_result(self, items, count, params):
        return dict(count=count, items=items, params=params)

    def _make_place_distance_item(self, place, params):
        latitude, longitude = parameters.get_position_from_dict(params.get_api_params())
        distance = gis_core.calculate_distance(longitude, latitude, place.longitude(), place.latitude())
        item = dict(place=place, distance=distance)
        return item

    def _get_max_id(self):
        return models.Message.objects.aggregate(max_id=Max('id'))["max_id"]


class MessageService(FeedService):

    default_limit = settings.DEFAULT_PAGINATE_BY

    def __init__(self, city_service, categorization_service):
        self.city_service = city_service
        self.categorization_service = categorization_service

    def get_place_messages(self, place, current_max_id=None, default_limit=None, **kwargs):
        if current_max_id is None:
            current_max_id = self._get_max_id()
        if default_limit is None:
            default_limit = self.default_limit
        params = parameters.PlaceMessagesParametersFactory.create(
            kwargs, self.categorization_service, current_max_id, default_limit)
        messages, count = queries.place_messages(place, **params.get_db_params())
        return self._make_result(messages, count, params.get_api_params())

    def search(self, place, current_max_id=None, default_limit=settings.DEFAULT_PAGINATE_BY, **kwargs):
        pass


class NewsFeedService(FeedService):

    news_items_default_limit = 17
    news_item_default_size = 3
    place_news_default_limit = 9
    gallery_preview_default_size = 9

    def __init__(self, message_service):
        self.message_service = message_service

    def __make_feed_item(self, place, params):
        messages = self.message_service.get_place_messages(place, **params.get_api_params())
        item = self._make_place_distance_item(place, params)
        item['messages'] = messages
        return item

    def __make_feed_item_with_gallery_preview(self, place, params):
        item = self.__make_feed_item(place, params)
        kwargs = params.get_api_params()
        kwargs[params_names.PHOTO] = True
        kwargs[params_names.LIMIT] = self.gallery_preview_default_size
        kwargs[params_names.OFFSET] = 0
        photos = self.message_service.get_place_messages(place, **kwargs)
        item['photos'] = photos
        return item

    def get_news(self, **kwargs):
        current_max_id = self._get_max_id()
        params = parameters.NewsFeedParametersFactory.create(
            kwargs, self.message_service.categorization_service, self.message_service.city_service,
            current_max_id, self.news_items_default_limit)
        places, count = queries.places_news_feed(**params.get_db_params())
        kwargs.pop(params_names.LIMIT)
        kwargs.pop(params_names.OFFSET)
        item_params = parameters.PlaceNewsFeedParametersFactory.create(
            kwargs, self.message_service.categorization_service, current_max_id, self.news_item_default_size)
        feed = self._make_result(
            [self.__make_feed_item(place, item_params)
             for place in places], count, params.get_api_params())
        return feed

    def get_place_news(self, place, **kwargs):
        current_max_id = self._get_max_id()
        params = parameters.PlaceNewsFeedParametersFactory.create(
            kwargs, self.message_service.categorization_service, current_max_id, self.place_news_default_limit)
        item = self.__make_feed_item_with_gallery_preview(place, params)
        return item


class PlaceService(FeedService):

    def __init__(self, city_service):
        self.city_service = city_service

    def search(self, **kwargs):
        params = parameters.PlaceSearchParametersFactory.create(kwargs, self.city_service)
        places = queries.places(**params.get_db_params())
        return [self._make_place_distance_item(place, params) for place in places]

    def search_in_venues(self, **kwargs):
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
