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


class CatigorizationServiceTest(TestCase):
    def setUp(self):
        self.categories = [
            models.Category(alias=u"outdoor", name=u"Верхняя одежда",
                keywords=u"Дубленка, Шуба, Пуховик, Зимняя куртка"),
            models.Category(alias=u"trousers", name=u"Брюки",
                keywords=u"Брюки, Штаны, Капри, Карго, Леггинсы, Лосины, Хакама, Шаровары, Джинсы, Скинни, Бэгги, Джегенсы"),
            models.Category(alias=u"socks", name=u"Чулочно-носочное",
                keywords=u"Носки, Портянки, Гольфы, Гетры, Чулки, Колготки, Термобелье, Рейтузы"),
        ]
        self.categorizationService = services.CategorizationService(self.categories)
    def test_get_all_stems(self):
        termo = self.categorizationService._get_all_stems(u"термобелье")
        self.assertSetEqual(set([u'термобел',]), termo)
        jacket = self.categorizationService._get_all_stems(u"куртка")
        self.assertSetEqual(set([u'куртк', u'курток', u'курточк']), jacket)
    def test_category_stems(self):
        stems = self.categorizationService.stems_ru[0][u"stems"]
        print stems
        print u', '.join([u' '.join([u'-'.join(form) for form in stem_group]) for stem_group in stems])
        self.assertSetEqual(stems[0][0], set([u'дубленок', u'дубленк', u'дубленочк']))
        self.assertSetEqual(stems[1][0], set([u'шуб']))
        self.assertSetEqual(stems[3][1], set([u'куртк', u'курток', u'курточк']))
    def test_detect_thing(self):
        message = models.Message(id=1, text=u"купил маЁчку, носок и пакет трусов, доволен как лось!")
        detected_things = self.categorizationService.detect_things(message)
        self.assertEquals(len(detected_things), 3)
