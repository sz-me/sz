# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.client import RequestFactory
from sz.api import views

"""
class DomainTagServicesTest(TestCase):
    def setUp(self):
        print u'[SETUP]'
        self.tags = [
            DomainTag(name = u'майка'),
            DomainTag(name = u'обувь'),
            DomainTag(name = u'шапка')]
        map(lambda tag: tag.save(), self.tags)
        
        self.tags[0].pattern_set.create(value = u'май')
        self.tags[1].pattern_set.create(value = u'болотник')
        self.tags[2].pattern_set.create(value = u'шапк')
        self.tags[2].pattern_set.create(value = u'шапочк')
        

    def print_tags(self):
        print lists.debug_info(
            lambda tag: u'#%s (%s)' % (tag.name, string.joinfields(map(lambda p: p.value, tag.pattern_set.all()), ',')), 
            self.tags, 
            u'Словарь:'
            )
        
    def test_lower_case_char_field(self):
        tag = DomainTag(name = u'ФутБолка')
        self.assertEqual(tag.name, u'футболка')
        
    def test_tags2dict(self):
        dict = services.tags2dict(self.tags)
        self.assertEqual(
            dict, 
            {
                u'майка': [u'май'], 
                u'обувь':[u'болотник'], 
                u'шапка':[u'шапк', u'шапочк'] 
            })
    
    def test_regexp_tagging_service(self):
        print '[REGEXP]'
        self.print_tags()
        message = u'Спининги, болотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = services.regexp_tagging_service(message, self.tags)
        print u'Тэги: ' + string.joinfields(tags, ', ')
        self.assertEqual(tags, [u'обувь'])
   
    def test_spell_tagging_service(self):
        print '[SPELL]'
        self.print_tags()
        message = u'Спининги, балотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = services.spellcorrector_tagging_service(message, self.tags)
        print u'Тэги: ' + string.joinfields(tags, ', ') 
        self.assertEqual(tags, [u'обувь'])
"""
position = {
    'latitude': 50.2616113,
    'longitude': 127.5266082,
    'accuracy': 0,
    }

class PlaceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_places_view(self):
        request = self.factory.get('/places/', position)
        view = views.PlaceRootNewsFeed.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


from sz.api import serializers
class SerializersTest(TestCase):
    def test_city_search(self):
        data1 = {
            'latitude': 50.2616113,
            'longitude': 127.5266082,
            'query': None
        }
        serializer = serializers.CitySearchSerializer(data1)
        self.assertTrue(serializer.is_valid())

        data2 = {
            'latitude': 50.2616113,
            'longitude': None,
            'query': 'Blagoveshch'
        }
        serializer = serializers.CitySearchSerializer(data2)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors, {'non_field_errors': [u'Latitude and longitude or query required']})

        data3 = {
            'longitude': None,
            'query': 'Blagoveshch'
        }
        serializer = serializers.CitySearchSerializer(data3)
        self.assertTrue(serializer.is_valid())

    def test_message_serializer(self):
        data = {
            u"text": u"джинсы по цене носков!",
            u"latitude": 50.261957910406444,
            u"longitude": 127.53488266715124,
            u"accuracy": 10.0,
            u"city_id": 2026609,
            u"place_id": u"4c636f6f79d1e21e62cbd815",
        }
        serializer = serializers.MessageSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg = serializer.errors)




    