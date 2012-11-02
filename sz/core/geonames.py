# -*- coding: utf-8 -*-
import urllib
import simplejson as json

class GeoNamesApi(object):
    """GeoNames API wrapper"""
    def __init__(self, config):
        self.geonames_api_uri = config['API_URI']
        self.username = config['USERNAME']

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
        response = f.read()
        return response

    def __get_json_result(self, service, params):
        uri = self.get_uri(service, params)
        response = self.__get(uri)
        result = json.loads(response)
        return result

    def find_nearby_place_name_json(self, params):
        #'style': 'SHORT'
        return self.__get_json_result('findNearbyPlaceName', params)

    def search_json(self, params):
        return self.__get_json_result('search', params)

