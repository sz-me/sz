# -*- coding: utf-8 -*-
import urllib
import simplejson as json
from sz.settings import GEONAMES_CONFIG

class GeoNamesWrapper(object):
    """GeoNames API wrapper"""

    geonames_api_uri = GEONAMES_CONFIG['API_URI']
    username = GEONAMES_CONFIG['USERNAME']

    def get_uri(self, resource, get_params = {}, json = True):
        if json:
            json_postfix = "JSON"
        else:
            json_postfix = ""
        get_params["username"] = self.username
        get_params_str = urllib.urlencode(get_params)
        uri = "{API_URI}{RESOURCE}{JSON_POSTFIX}?{GET_PARAMS}".format(
            API_URI = self.geonames_api_uri,
            RESOURCE = resource,
            JSON_POSTFIX = json_postfix,
            GET_PARAMS = get_params_str
        )
        return uri

    def __get(self, uri):
        f = urllib.urlopen(uri)
        r = f.read()
        response = json.loads(r)
        return response

    def find_nearby_place_name_json(self, lat, lng):
        params = {
            'lat': lat,
            'lng': lng,
            'style': 'SHORT'
        }
        uri = self.get_uri('findNearbyPlaceName', params)
        return self.__get(uri)

