# -*- coding: utf-8 -*-
from sz.core import lists, morphology
from sz.core.morphology import stemmers
import re

non_word_pattern = re.compile(r'\W+', flags=re.U)

class CategorizationService:
    def __init__(self, categories):
        #self.categories = categories
        self.sremmer_ru = stemmers.RussianStemmer()
        #self.sremmer_ru.stemWord(word)
        self.stems_ru = map(lambda category: {
            u"category": category,
            u"stems": self._category_stems(category)
        }, categories )
    def _get_all_stems(self, word):
        stem = self.sremmer_ru.stemWord(word)
        all_stems = set([stem,])
        addition = morphology.addition_for_ended_in_k(stem)
        if addition:
            all_stems = all_stems | addition
        return all_stems
    def _category_stems(self, category):
        phrases = [
            [ self._get_all_stems(word) for word in non_word_pattern.split(keyword.strip())]
            for keyword in category.keywords.split(u',')]
        return phrases
    def _make_phrase_pattern(self, phrase):
        pattern = ur"\w*\W*".join([ ur'(%s)' % ur'|'.join(word_set) for word_set in phrase ])
        print pattern
        return pattern
    """
        Определяет какой вещи соответствует слово, если никакой, то возвращает None
    """
    def _detect_thing_in_word_ru(self, word):
        for thing in self.things:
            if word.startswith(thing.stem) or\
               morphology.addition_for_ended_in_k(thing.stem) and\
               lists.any(lambda form:
               word.startswith(form),
                   morphology.addition_for_ended_in_k(thing.stem)):
                return thing
        return None

    def parse_text(self, text):
        words = set(morphology.extract_words_ru(text))
        things = set([])
        stems = set([])
        for word in words:
            if len(word) > 2:
                thing = self._detect_thing_in_word_ru(word)
                if thing:
                    things.add(thing)
                else:
                    stem = self.sremmer_ru.stemWord(word)
                    stems.add(stem)
                    addition = morphology.addition_for_ended_in_k(stem)
                    if addition:
                        for form in addition:
                            stems.add(form)
        return things, stems

    def detect_things(self, message):
        things, stems = self.parse_text(message.text)
        message.things.clear()
        for thing in things:
            message.things.add(thing)
        return things

    def get_with_additional_things(self, things):
        categories = set([thing.category for thing in things])
        things_many = [category.thing_set.all() for category in categories]
        return set([el for lst in things_many for el in lst])


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


