# -*- coding: utf-8 -*-
from django.test import TestCase
from sz.core.morphology import stemmers
from sz.core import models, services

russian_stemmer = stemmers.RussianStemmer()

class StemmerTest(TestCase):
    def test_russian(self):
        print russian_stemmer.stemWord(u'маечка')
        print russian_stemmer.stemWord(u'майка')
        print russian_stemmer.stemWord(u'Майк')
        print russian_stemmer.stemWord(u'палаточка')
        self.assertEquals(russian_stemmer.stemWord(u'майка'), u'майк')


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
        detected_things = self.categorizationService.detect_things(self.thinks, message)
        self.assertEquals(len(detected_things), 1)
