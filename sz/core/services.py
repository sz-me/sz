# -*- coding: utf-8 -*-
from sz.core import utilities
from sz.core.algorithms import lists

class CategorizationService:
    def detect_thinks(self, things, message):
        words = set(utilities.words(message.text))
        detected_things = filter(
            lambda think: lists.any(
                lambda word: word.startswith(think.stem),
                words),
            things
        )
        for thing in detected_things:
            message.things.add(thing);
        return detected_things