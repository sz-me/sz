# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth import models as auth_models
from sz.core import models
from sz.core import gis as gis_core


class MessageTest(TestCase):
    def setUp(self):
        user = auth_models.User()
        user.save()
        self.user = user
        place = models.Place(id='test', name='test', contact='', address='', crossStreet='',
                             position=gis_core.ll_to_point(128, 56), city_id=2026609,
                             foursquare_icon_suffix='', foursquare_icon_prefix='')
        place.save()
        self.place = place
        smile = models.Smile(emotion='lol')
        smile.save()
        self.smile = smile

    def test_strip_text(self):
        message = models.Message(text=u" Пробельчики до и после ", user=self.user, place=self.place, smile=self.smile)
        message.save()
        self.assertEqual(message.text, u"Пробельчики до и после")
