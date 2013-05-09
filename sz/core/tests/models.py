# -*- coding: utf-8 -*-
from django.test import TestCase
from sz.core.models import *
from sz.core import gis as gis_core


class MessageTest(TestCase):
    def setUp(self):
        user = User()
        user.save()
        self.user = user
        place = Place(id='test', name='test', contact='', address='', crossStreet='',
                      position=gis_core.ll_to_point(128, 56), city_id=2026609,
                      foursquare_icon_suffix='', foursquare_icon_prefix='')
        place.save()
        self.place = place
        smile = Smile(emotion='lol')
        smile.save()
        self.smile = smile

    def test_strip_text(self):
        message = Message(
            text=u" Пробельчики до и после ", user=self.user,
            place=self.place, smile=self.smile
        )
        message.save()
        self.assertEqual(message.text, u"Пробельчики до и после")


class RegistrationTest(TestCase):
    def test_verify(self):
        email = 'test@test.com'
        user = RegistrationProfile.objects.create_unverified_user(
            email,
            'password',
            Style.objects.get(pk=1)
        )
        self.assertEqual(user.email, email)
        self.assertFalse(user.is_verified)
        self.assertTrue(RegistrationProfile.objects.filter(
            user=user).exists())
        profile = user.registrationprofile_set.all()[0]
        RegistrationProfile.objects.confirm_email(
            profile.confirmation_key
        )
        user = User.objects.get(id=user.id)
        self.assertTrue(user.is_verified)
        profile = user.registrationprofile_set.all()[0]
        self.assertEqual(
            profile.confirmation_key,
            profile.CONFIRMED
        )
