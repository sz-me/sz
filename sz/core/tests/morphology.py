# -*- coding: utf-8 -*-
from django.test import TestCase
from sz.core.morphology import stemmers
from sz.core import models, morphology, services

class MorphUtilsTest(TestCase):
    def test_extract_words_ru(self):
        text = u'съешь ещё этих мягких французских булочек с маслом, please'
        self.assertEqual(morphology.extract_words_ru(text),
            set([u'маслом', u'съешь', u'булочек', u'французских', u'мягких']))

    def test_replace_last(self):
        top = u'майк'
        self.assertEquals(morphology.replace_last(top, 2, u'ечк'), u'маечк')
        shirt = u'футболк'
        self.assertEquals(morphology.replace_last(shirt, 1, u'очк'), u'футболочк')
    def test_addition_for_ended_in_k(self):
        self.assertEquals(morphology.addition_for_ended_in_k(
            u'майк'), set([u'маечк', u'маек']))
        self.assertEquals(morphology.addition_for_ended_in_k(
            u'рубашк'), set([u'рубашечк', u'рубашек']))
        self.assertEquals(morphology.addition_for_ended_in_k(
            u'футболк'), set([u'футболочк', u'футболок']))

russian_stemmer = stemmers.RussianStemmer()

class StemmerTest(TestCase):
    def test_russian(self):
        print russian_stemmer.stemWord(u'маечка')
        print russian_stemmer.stemWord(u'майка')
        print russian_stemmer.stemWord(u'Майк')
        print russian_stemmer.stemWord(u'палаточка')
        self.assertEquals(russian_stemmer.stemWord(u'майка'), u'майк')

class RussianStemmerServiceTest(TestCase):
    def setUp(self):
        self.stemmer = services.RussianStemmerService()
    def test_get_all_stems(self):
        termo = self.stemmer.get_all_stems(u"термобелье")
        self.assertSetEqual(set([u'термобел',]), termo)
        jacket = self.stemmer.get_all_stems(u"куртка")
        self.assertSetEqual(set([u'куртк', u'курток', u'курточк']), jacket)

class StemmingServiceMock:
    def __init__(self):
        self.stem_dictionary = {
            u'куртка': set([u'куртк', u'курток', u'курточк']),
            u'платье': set([ur'плат',]),
            u'зимняя': set([ur'зимн',]),
            u'пальто': set([ur'пальто',]),
            u'костюм': set([ur'костюм',]),
            u'дублёнка': set([u'дубленок', u'дубленк', u'дубленочк']),
            u'шуба': set([u'шуб']),
            }
    def get_all_stems(self, word):
        all_stems = self.stem_dictionary.get(word, set([ur'stem',]))
        return all_stems

import re
class CatigorizationServiceTest(TestCase):
    def setUp(self):
        categories = [
            models.Category(alias=u"outdoor", name=u"Верхняя одежда",
                keywords=u"Дубленка, Шуба, Пуховик, Зимняя куртка"),
            models.Category(alias=u"trousers", name=u"Брюки",
                keywords=u"Брюки, Штаны, Джинсы"),
            models.Category(alias=u"socks", name=u"Чулочно-носочное",
                keywords=u"Носки, Портянки, Гольфы, Гетры, Чулки, Колготки, Термобелье, Рейтузы"),
        ]
        stemmingService = StemmingServiceMock()
        self.categorizationService = services.CategorizationService(categories, stemmingService)
    def test_make_phrase_pattern(self):
        phrase = [set([u'зимн']), set([u'куртк', u'курток', u'курточк'])]
        pattern = self.categorizationService._make_phrase_pattern(phrase)
        self.assertEqual(pattern, ur'(зимн)\w*\W*(куртк|курток|курточк)')
        self.assertTrue(re.search(pattern, u'купил зимнюю куртку!', flags=re.U))
    def test_detect_categories(self):
        text=u"купил ШУБУ жене!"
        detected_categories = self.categorizationService.detect_categories(text)
        print u", ".join([category.name for category in detected_categories])
        self.assertEquals(len(detected_categories), 1)
