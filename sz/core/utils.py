from sz import settings


DEFAULT_PAGINATE_BY = settings.DEFAULT_PAGINATE_BY


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except Exception:
        return default


def safe_get(val, func, default=None):
    try:
        return func(val)
    except Exception:
        return default


def get_paging_args(**kwargs):
    limit = safe_cast(kwargs.get('limit', DEFAULT_PAGINATE_BY), int, DEFAULT_PAGINATE_BY)
    offset = safe_cast(kwargs.get("offset", 0), int, 0)
    max_id = kwargs.get("max_id", None)
    return limit, offset, max_id


def get_position_from_kwargs(**kwargs):
    latitude = kwargs.get('latitude', None)
    longitude = kwargs.get('longitude', None)
    assert latitude and longitude, 'latitude and longitude are required'
    return latitude, longitude