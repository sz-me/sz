# -*- coding: utf-8 -*-
import re

def maketransU(s1, s2, todel=""):
    trans_tab = dict( zip( map(ord, s1), map(ord, s2) ) )
    trans_tab.update( (ord(c),None) for c in todel )
    return trans_tab

TRANSLATE_TABLE_RU = maketransU([u"ё"], [u"е"])
VOWEL_RU = set(u"аеиоуыэюя")
CONSONANT_RU = set(u"бвгджзйклмнпрстфхцчшщ")
HUSHING_RU = set(u"жчшщ")
J_RU = set(u"й")
ALPHABET_RU = VOWEL_RU | CONSONANT_RU | set(u"ъь")
STOP_WORDS3_RU = set([
    u'этот', u'этого', u'этому', u'этим', u'этом', u'это',
    u'эта', u'эту', u'этой',
    u'эти', u'этим', u'этих',
    u'тот', u'того', u'тому', u'тем', u'том', u'этой',
    u'теми', u'тех',
    u'что', u'чем',
    u'кто', u'кого', u'кем', u'ком',
    u'как', u'какой', u'какими'
    u'так', u'такой', u'такими',
    u'над', u'под', u'для',
    u'она', u'оно', u'ней', u'них', u'ими',
    u'еще',
    ])

SPACE_REGEX = re.compile('[^\w]|[+]', re.U)
WORD_REGEX_RU = re.compile(u"[%s]{3,}" % "".join(ALPHABET_RU), re.U)

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

def extract_words_ru(text):
    text = text.lower().translate(TRANSLATE_TABLE_RU)
    words = set(WORD_REGEX_RU.findall(text))
    return words - STOP_WORDS3_RU

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