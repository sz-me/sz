# -*- coding: utf-8 -*-
from django.test import TestCase
from sz.core.gis import geonames, venue
from sz.settings import GEONAMES_API_CONFIG

position = {
    'latitude': 50.2616113,
    'longitude': 127.5266082,
    'accuracy': 50
}
'''
class GeoServicesTest(TestCase):
    def test_search_venues(self):
        result = venue.search(position, None, None)
        print u'МЕСТА (%s)' % len(result[u'venues'])
        i = 1
        print ";\n".join(["%s, %s (%s, %s)" %
                          (
                              v[u'name'],
                              v[u'location'].get(u'address'),
                              v[u'location'].get(u'lat'),
                              v[u'location'].get(u'lng'),
                              ) for v in result[u'venues']])
        self.assertTrue(result)

class GeoNamesTest(TestCase):
    def setUp(self):
        self.geoNamesApi = geonames.GeoNamesApi(GEONAMES_API_CONFIG)
        self.params = {
            'lat': position['latitude'],
            'lng': position['longitude'],
            'style': 'MEDIUM'
        }

    def test_uri(self):

        uri = self.geoNamesApi.get_uri('findNearbyPlaceName', self.params)
        #print uri
        self.assertEquals(uri, 'http://api.geonames.org/findNearbyPlaceNameJSON?lat=50.2616113&username=sz.me&lng=127.5266082&style=MEDIUM')

    def test_find_nearby_place_name_json(self):
        r = self.geoNamesApi.find_nearby_place_name_json(self.params)
        print r
        city = r['geonames'][0]['name']
        self.assertTrue(city, 'Blagoveshchensk')

    def test_search(self):
        params = { 'name_startsWith': 'Blagoveshchensk', 'maxRows': 10, 'style': 'MEDIUM' }
        r = geonames.search('Blagoveshchensk')#self.geoNamesApi.search_json(params)
        print r
        print ".\n".join([u"%s,%s,%s (%f,%f) geonameId=%i, toponymName='%s'" % (
            g['name'],
            g['adminName1'],
            g['countryCode'],
            g['lat'],
            g['lng'],
            g['geonameId'],
            g['toponymName']
            ) for g in r['geonames']])
        self.assertTrue(r)
'''
