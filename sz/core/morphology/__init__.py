# -*- coding: utf-8 -*-
import re

def maketransU(s1, s2, todel=""):
    trans_tab = dict( zip( map(ord, s1), map(ord, s2) ) )
    trans_tab.update( (ord(c),None) for c in todel )
    return trans_tab

TRANSLATE_TABLE_RU = maketransU(u"ё", u"е")
VOWEL_RU = set(u"аеиоуыэюя")
CONSONANT_RU = set(u"бвгджзйклмнпрстфхцчшщ")
HUSHING_RU = set(u"жчшщ")
J_RU = set(u"й")
ALPHABET_RU = VOWEL_RU | CONSONANT_RU | set(u"ъь")

SPACE_REGEX = re.compile('[^\w]|[+]', re.U)

def extract_words(text):
    """
    Разбивает текст на слова. Пунктуация игнорируется.
    Пример использования::

        from pymorphy.contrib import tokenizers

        for word in tokenizers.extract_words(text):
            print word

    Возвращает генератор, выдающий слова из текста (не list).

    """
    for word in SPACE_REGEX.split(text):
        test_word = word.replace('-','')
        if not test_word or test_word.isspace() or test_word.isdigit():
            continue
        word = word.strip('-')
        yield word.lower().translate(TRANSLATE_TABLE_RU)

def replace_last(stem, count, str):
    return stem[:len(stem)-count] + str

def addition_for_ended_in_k(stem):
    stem_length = len(stem)
    if (stem_length > 2):
        if (stem[stem_length-1] == u'к'):
            if (stem[stem_length-2] in J_RU):
                return set([replace_last(stem, 2, u'ечк'), replace_last(stem, 2, u'ек')])
            elif (stem[stem_length-2] in HUSHING_RU):
                return set([replace_last(stem, 1, u'ечк'), replace_last(stem, 1, u'ек')])
            elif (stem[stem_length-2] in CONSONANT_RU):
                return set([replace_last(stem, 1, u'очк'), replace_last(stem, 1, u'ок')])
            elif (stem[stem_length-2] in VOWEL_RU):
                return set([replace_last(stem, 1, u'ч'),])
    return u''