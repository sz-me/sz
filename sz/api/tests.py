# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import RequestFactory
from sz.api import serializers
from sz.api.views import places as places_views


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
        view =places_views.PlaceRootNews.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class MessageSerializerTest(TestCase):
    def setUp(self):
        self.not_valid_message_data = dict(
            text='',
            photo=None,
            place="4c636f6f79d1e21e62cbd815"
        )

        self.valid_message_data = {
            u"text": u"джинсы по цене носков!",
            u"latitude": 50.261957910406444,
            u"longitude": 127.53488266715124,
            u"accuracy": 10.0,
            u"city_id": 2026609,
            u"place_id": u"4c636f6f79d1e21e62cbd815",
            u"smile": 1,
            }

    def test_validation(self):
        serializer = serializers.MessageSerializer(data=self.not_valid_message_data)
        self.assertFalse(serializer.is_valid(), 'Empty message addition is allow!!!')
        serializer = serializers.MessageSerializer(data=self.valid_message_data)
        self.assertTrue(serializer.is_valid(), msg = serializer.errors)


class RegistrationTest(TestCase):
    def test_registration_serializer(self):
        data = {
            'email': 'email@i.am',
            'style': 1,
            'password1': 'pass1',
            'password2': 'pass2'}
        serializer = serializers.RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())






    