# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase

class ListsTest(TestCase):
    def test_any(self):
        self.assertFalse(lists.any(lambda x: x < 0, [1, 2, 3]))
        self.assertFalse(lists.any(lambda x: x != None, [None, None, None]))
        self.assertTrue(lists.any(lambda x: x > 1, [0, 1, 2]))
    def test_all(self):
        self.assertTrue(lists.all(lambda x: x > 0, [1, 2, 3]))
        self.assertFalse(lists.all(lambda x: x == None, set([None, 1])))
        self.assertFalse(lists.all(lambda x: x > 1, [0, 1, 2]))
    def test_first(self):
        self.assertEquals(lists.first([4, 2, 3]), 4)
        self.assertEquals(lists.first(set([4, 5, 3, 'a', 18])), 'a')
    def test_last(self):
        self.assertEquals(lists.last([4, 2, 3]), 3)
    def test_first_match(self):
        self.assertEquals(lists.first_match(lambda x: x < 4, [4, 2, 3, 5]), 2)
        self.assertEquals(lists.first_match(lambda x: x < 1, [4, 2, 3, 5]), None)
    def test_last_match(self):
        self.assertEquals(lists.last_match(lambda x: x < 4, [4, 2, 3, 5]), 3)
        self.assertEquals(lists.last_match(lambda x: x > 7, [4, 2, 3, 5]), None)
"""
class TagsServicesTest(TestCase):
    def setUp(self):
        print u'[SETUP]'
        self.tags = { 
            u'майка': [u'май'], 
            u'обувь':[u'болотник'], 
            u'шапка':[u'шапк', u'шапочк'] }
    def print_tags(self):
        
        print lists.debug_info(
            lambda (tag, patterns): u'#%s (%s)' % (tag, string.joinfields([tag] + patterns, ',')), 
            self.tags.items(), 
            u'Словарь:'
            )
    def test_regexp(self):
        print '[REGEXP]'
        self.print_tags()
        message = u'Спининги, болотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = regexp_tagging_algorithm(message, self.tags) 
        print u'Тэги: ' + string.joinfields(tags, ', ')
        self.assertEqual(tags, [u'обувь'])
    
    def test_spellcorrector(self):
        print '[SPELL]'
        self.print_tags()
        message = u'Спининги, балотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = spellcorrector_tagging_algorithm(message, self.tags) 
        print u'Тэги: ' + string.joinfields(tags, ', ')
        self.assertEqual(tags, [u'обувь'])
"""

position = {
    'latitude': 50.2616113,
    'longitude': 127.5266082,
    'accuracy': 50
}
from sz.core import venue, lists

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


from sz.core import geonames
from sz.settings import GEONAMES_API_CONFIG

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

from sz.core.morphology import stemmers
russian_stemmer = stemmers.RussianStemmer()

class StemmerTest(TestCase):
    def test_russian(self):
        print russian_stemmer.stemWord(u'маечка')
        print russian_stemmer.stemWord(u'майка')
        print russian_stemmer.stemWord(u'Майк')
        print russian_stemmer.stemWord(u'палаточка')
        self.assertEquals(russian_stemmer.stemWord(u'майка'), u'майк')

from sz.core import models
from sz.core import services
class CatigorizationServiceTest(TestCase):
    def setUp(self):
        self.thinks = [
            models.Thing(
                tag=u'майка',
                stem = russian_stemmer.stemWord(u'майка')),
            models.Thing(
                tag=u'трусы',
                stem = russian_stemmer.stemWord(u'трусы')),
            models.Thing(
                tag=u'носки',
                stem = russian_stemmer.stemWord(u'носки')),
        ]
        self.categorizationService = services.CategorizationService()
    def test_detect_thing(self):
        message = models.Message(id=1, text=u"купил пакет трусов, доволен как лось!")
        detected_thinks = self.categorizationService.detect_thinks(self.thinks, message)
        self.assertEquals(len(detected_thinks), 1)