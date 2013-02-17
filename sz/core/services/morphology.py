# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ObjectDoesNotExist
from sz.core import morphology, models
from sz.core.morphology import stemmers


class StemmingService:

    def __init__(self, stemmer, word_extract_handler, language):
        self.stemmer = stemmer
        self.word_extract = word_extract_handler
        self.language = language

    def get_all_stems(self, word):
        self.stemmer.stemWord(word)

    def get_main_stem(self, word):
        self.stemmer.stemWord(word)

    def get_all_stems_for_text(self, text):
        words = self.word_extract(text)
        return set([stem for word in words for stem in self.get_all_stems(word)])


class RussianStemmingService(StemmingService):

    def __init__(self):
        stemmer = stemmers.RussianStemmer()
        StemmingService.__init__(self, stemmer, morphology.extract_words_ru, models.LANGUAGE_CHOICES[1][0])

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
        }, categories)

    def get_categories(self):
        return [kw[u"category"] for kw in self.keywords_ru]

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
                    for word in self.non_word_pattern.split(keyword)
                ]

                for keyword in category.get_keywords_list()
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
        pattern = ur"\w*\W*".join([self._replace_vowel_ru(ur'(%s)' % ur'|'.join(word_set)) for word_set in phrase])
        return pattern

    def _has_matches(self, text, patterns):
        matches = filter(lambda x: x.search(text), patterns)
        return matches

    def detect_categories(self, text):
        matches = filter(lambda x: self._has_matches(text, x[u"patterns"]), self.keywords_ru)
        return map(lambda x: x[u"category"], matches)

    def detect_stems(self, text):
        stems = self.russianStemmingService.get_all_stems_for_text(text)
        language = self.russianStemmingService.language
        return [(stem, language) for stem in stems]

    def assert_stems(self, message):
        message.stems.clear()
        stems = self.detect_stems(message.text)
        for s in stems:
            try:
                stem = models.Stem.objects.get(language=s[1], stem=s[0])
            except ObjectDoesNotExist:
                stem = models.Stem(language=s[1], stem=s[0])
                stem.save()
            message.stems.add(stem)
        return message
