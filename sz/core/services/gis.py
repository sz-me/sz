# -*- coding: utf-8 -*-
from sz.core.gis import geonames


class GeonamesCityService:
    response = lambda g : {
        "id": g['geonameId'],
        "name": g['name'],
        "region": g['adminName1'],
        "country": g['countryName'],
        "country_code": g['countryCode'],
        "latitude": g['lat'],
        "longitude": g['lng'],
        "geoname_id": g['geonameId'],
        "international_name": g['toponymName']
    }
    def get_city_by_position(self, longitude, latitude):
        response = geonames.nearby({'latitude':latitude, 'longitude': longitude})
        response = [ self.response(g) for g in response['geonames']]
        assert len(response) > 0, \
            "In position (%s, %s) a city is not detected" % (longitude, latitude)
        return response[0]
    def search(self, query):
        request = geonames.search(query)
        return [ self.response(g) for g in request['geonames']]


class BlagoveshchenskCityService:
    def get_city_by_position(self, longitude, latitude):
        return {"id": 2026609}
    def search(self, query):
        return [ {"id": 2026609}, ]
