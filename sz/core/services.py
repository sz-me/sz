# -*- coding: utf-8 -*-
import re, string
from sz.core import lists,morphology
from sz.core.morphology import stemmers


class StemmerService:
    def __init__(self, stemmer):
        self.stemmer = stemmer
    def get_all_stems(self, word):
        self.stemmer.stemWord(word)
    def get_main_stem(self, word):
        self.stemmer.stemWord(word)

class RussianStemmerService(StemmerService):
    def __init__(self):
        stemmer = stemmers.RussianStemmer()
        StemmerService.__init__(self, stemmer)
    def get_all_stems(self, word):
        stem = self.stemmer.stemWord(word)
        all_stems = set([stem,])
        addition = morphology.addition_for_ended_in_k(stem)
        if addition:
            all_stems = all_stems | addition
        return all_stems

class CategorizationService:
    """
    This is a service that detects text categories by keywords, contained in the text
    """
    non_word_pattern = re.compile(r'\W+', flags=re.U)
    def __init__(self, categories, russianStemmingService):
        self.russianStemmingService = russianStemmingService
        self.keywords_ru = map(lambda category: {
            u"category": category,
            u"patterns": map(
                lambda x: re.compile(self._make_phrase_pattern(x), flags=re.U|re.I),
                self._category_stems(category))
        }, categories )
    def _get_all_stems(self, word):
        all_stems = self.russianStemmingService.get_all_stems(word)
        return all_stems
    """
    Return a list of all stems for category (for each keyword from the category)
    """
    def _category_stems(self, category):
        phrases = \
        [
            [
                self._get_all_stems(word)
                    for word in self.non_word_pattern.split(keyword.strip())
            ]

            for keyword in category.keywords.split(u',')
        ]
        return phrases
    def _replace_vowel_ru(self, word):
        replace_table_ru = {
            u'а': u'[ао]',
            u'о': u'[ао]',
            u'е': u'[еёи]',
            u'ё': u'[её]',
        }
        new_word = ""
        for sign in word:
            new_word += replace_table_ru.get(sign, sign)
        return new_word
    def _make_phrase_pattern(self, phrase):
        # todo считать за одну букву [ао] и [еёи]
        pattern = ur"\w*\W*".join([ self._replace_vowel_ru(ur'(%s)' % ur'|'.join(word_set)) for word_set in phrase ])
        return pattern
    def _has_matches(self, text, patterns):
        matches = filter(lambda x: x.search(text), patterns)
        return matches
    def detect_categories(self, text):
        matches = filter(lambda x: self._has_matches(text, x[u"patterns"]), self.keywords_ru)
        return map(lambda x: x[u"category"], matches)

from django.utils import timezone
class ModelCachingService:
    stored = []
    cached = []
    for_insert = []
    for_update = []
    def __init__(self, data, date, delta):
        assert data, 'data is required'
        if(len(data) > 0):
            assert date, 'date is required'
            assert delta, 'delta is required'
            data = set(data)
            model_class = type(lists.first(data))
            assert lists.all(lambda e: type(e) == model_class , data), \
                'data contain items of different types'
            self.stored = model_class.objects.filter(pk__in=[e.id for e in data])
            db = map(lambda e: dict(pk=e.id, date=date(e)), self.stored)
            non_cached_entities = set(filter(lambda e:
                e.pk not in [x['pk'] for x in db], data))
            self.cached = data - non_cached_entities
            last_update_date = lambda e: \
                filter(lambda x: x['pk'] == e.pk, db)[0]['date']
            expired_places = filter(lambda e:
                timezone.now() - last_update_date(e) > delta, self.cached)

            self.for_insert = non_cached_entities
            self.for_update = expired_places

    def save(self):
        map(lambda e: e.save(force_insert=True), self.for_insert)
        map(lambda e: e.save(force_update=True), self.for_update)


