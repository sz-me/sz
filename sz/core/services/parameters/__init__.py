from sz.core import utils, models
from sz.core.services.parameters import names as params_names


def get_paging_from_dict(args):
    to_int = lambda name: utils.safe_cast(args.get(name, None), int, None)
    to_none_if_neg_int = lambda v: v and (v > 0 and v or None) or None
    to_pos_int = lambda name: to_none_if_neg_int(to_int(name))
    limit = to_pos_int(params_names.LIMIT)
    offset = to_pos_int(params_names.OFFSET)
    max_id = to_pos_int(params_names.MAX_ID)
    return limit, offset, max_id


def get_position_from_dict(args):
    latitude = args.get(params_names.LATITUDE, None)
    longitude = args.get(params_names.LONGITUDE, None)
    assert latitude and longitude, 'latitude and longitude are required'
    return latitude, longitude


class ParametersGroupBase:

    def __init__(self, params):
        self.params = params

    def get_db_params(self):
        pass

    def get_api_params(self):
        pass


class ParametersGroupDecorator(ParametersGroupBase):

    def __init__(self, params, component=None):
        ParametersGroupBase.__init__(self, params)
        self.__component = component

    def get_db_params(self):
        if self.__component:
            return self.__component.get_db_params()
        else:
            return dict()

    def get_api_params(self):
        if self.__component:
            return self.__component.get_api_params()
        else:
            return dict()


class PositionDecorator(ParametersGroupDecorator):

    def __init__(self, params, component=None):
        ParametersGroupDecorator.__init__(self, params, component)
        self._latitude, self._longitude = get_position_from_dict(self.params)

    def __get_params(self, params):
        params[params_names.LATITUDE] = self._latitude
        params[params_names.LONGITUDE] = self._longitude
        return params

    def get_db_params(self):
        params = ParametersGroupDecorator.get_db_params(self)
        return self.__get_params(params)

    def get_api_params(self):
        params = ParametersGroupDecorator.get_api_params(self)
        return self.__get_params(params)


class LocationDecoratorBase(PositionDecorator):

    def __init__(self, params, city_service, component=None):
        PositionDecorator.__init__(self, params, component)
        self.__city_service = city_service
        self._radius = utils.safe_cast(params.get(params_names.RADIUS, None), int, None)
        if self._radius is not None:
            if self._radius <= 0:
                self._radius = None

    def _get_city(self):
        city = self.__city_service.get_city_by_position(self._longitude, self._latitude)
        return city

    def get_api_params(self):
        params = PositionDecorator.get_api_params(self)
        if self._radius is not None:
            params[params_names.RADIUS] = self._radius
        return params


class LocationDecorator(LocationDecoratorBase):

    def get_db_params(self):
        params = LocationDecoratorBase.get_db_params(self)
        params[params_names.RADIUS] = self._radius
        if self._radius is None:
            city = self._get_city()
            params[params_names.CITY_ID] = city['id']
        return params


class LocationAlwaysWithCityDecorator(LocationDecoratorBase):

    def get_db_params(self):
        params = LocationDecoratorBase.get_db_params(self)
        params[params_names.RADIUS] = self._radius
        city = self._get_city()
        params[params_names.CITY_ID] = city['id']
        return params


class PagingDecorator(ParametersGroupDecorator):

    def __init__(self, params, current_max_id, default_limit, component=None):
        ParametersGroupDecorator.__init__(self, params, component)
        self.__limit, self.__offset, self.__max_id = get_paging_from_dict(self.params)
        self.__current_max_id = current_max_id
        self.__default_limit = default_limit

    def __get_params(self, params):
        params[params_names.MAX_ID] = self.__max_id or self.__current_max_id
        params[params_names.LIMIT] = self.__limit or self.__default_limit
        params[params_names.OFFSET] = self.__offset or 0
        return params

    def get_db_params(self):
        params = ParametersGroupDecorator.get_db_params(self)
        return self.__get_params(params)

    def get_api_params(self):
        params = ParametersGroupDecorator.get_api_params(self)
        return self.__get_params(params)


class ContentDecorator(ParametersGroupDecorator):

    def __init__(self, params, categorization_service, component=None):
        ParametersGroupDecorator.__init__(self, params, component)
        self.__categorization_service = categorization_service
        self.__category = params.get(params_names.CATEGORY, None)
        self.__query = params.get(params_names.QUERY, None)
        self.__photo = params.get(params_names.PHOTO, None)

    def get_db_params(self):
        params = ParametersGroupDecorator.get_db_params(self)
        params[params_names.STEMS] = []
        if self.__query:
            if self.__query.strip != '':
                params[params_names.STEMS] = self.__categorization_service.detect_stems(self.__query)
        if isinstance(self.__category, models.Category):
            params[params_names.CATEGORY] = self.__category
        else:
            params[params_names.CATEGORY] = None
        if self.__photo:
            params[params_names.PHOTO] = True
        else:
            params[params_names.PHOTO] = None
        return params

    def get_api_params(self):
        params = ParametersGroupDecorator.get_api_params(self)
        if self.__query:
            if self.__query.strip != '':
                params[params_names.QUERY] = self.__query
        if isinstance(self.__category, models.Category):
            params[params_names.CATEGORY] = self.__category
        else:
            params[params_names.CATEGORY] = None
        if self.__photo:
            params[params_names.PHOTO] = True
        return params


class PlaceNameDecorator(ParametersGroupDecorator):

    def __init__(self, params, component=None):
        ParametersGroupDecorator.__init__(self, params, component)
        self.__query = params.get(params_names.QUERY, None)

    def get_db_params(self):
        params = ParametersGroupDecorator.get_db_params(self)
        params[params_names.QUERY] = self.__query
        return params

    def get_api_params(self):
        params = ParametersGroupDecorator.get_api_params(self)
        params[params_names.QUERY] = self.__query
        return params


class PlaceMessagesParametersFactory:

    @classmethod
    def create(cls, params, categorization_service, current_max_id, default_limit):
        content_group = ContentDecorator(params, categorization_service)
        paging_group = PagingDecorator(params, current_max_id, default_limit, content_group)
        return paging_group


class PlaceNewsFeedParametersFactory:

    @classmethod
    def create(cls, params, categorization_service, current_max_id, default_limit):
        content_group = ContentDecorator(params, categorization_service)
        position_group = PositionDecorator(params, content_group)
        paging_group = PagingDecorator(params, current_max_id, default_limit, position_group)
        return paging_group


class NewsFeedParametersFactory:

    @classmethod
    def create(cls, params, categorization_service, city_service, current_max_id, default_limit):
        content_group = ContentDecorator(params, categorization_service)
        location_group = LocationDecorator(params, city_service, content_group)
        paging_group = PagingDecorator(params, current_max_id, default_limit, location_group)
        return paging_group


class PlaceSearchParametersFactory:

    @classmethod
    def create(cls, params, city_service):
        location_group = LocationAlwaysWithCityDecorator(params, city_service)
        place_name_group = PlaceNameDecorator(params, location_group)
        return place_name_group