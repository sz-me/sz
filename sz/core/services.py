# -*- coding: utf-8 -*-
from sz.core import lists, morphology

class CategorizationService:
    def detect_thinks(self, things, message):
        words = set(morphology.extract_words(message.text))
        detected_things = filter(
            lambda think: lists.any(
                lambda word: word.startswith(think.stem),
                words),
            things
        )
        for thing in detected_things:
            message.things.add(thing);
        return detected_things

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


