# -*- coding: utf-8 -*-
from sz.core import lists, morphology

class CategorizationService:
    def detect_things_in_text(self, things, text):
        words = set(morphology.extract_words(text))
        detected_things = filter(
            lambda think: lists.any(
                lambda word:
                    word.startswith(think.stem) or
                    morphology.addition_for_ended_in_k(think.stem) and lists.any(
                        lambda form: word.startswith(form),
                        morphology.addition_for_ended_in_k(think.stem)),
                filter(lambda word: len(word) > 2, words)),
            things
        )
        return detected_things
    def detect_things(self, things, message):
        detected_things = self.detect_things_in_text(things, message.text)
        message.things.clear()
        for thing in detected_things:
            message.things.add(thing)
        return detected_things
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


