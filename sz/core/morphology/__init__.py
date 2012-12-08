# -*- coding: utf-8 -*-
vowel_ru = set(u"аеиоуыэюя")
consonant_ru = set(u"бвгджзйклмнпрстфхцчшщ")
hushing_ru = set(u"жчшщ")
alphabet_ru = vowel_ru | consonant_ru | set(u"ъь")


import re
SPACE_REGEX = re.compile('[^\w_-]|[+]', re.U)

def extract_words(text):
    """
    Разбивает текст на слова. Пунктуация игнорируется.
    Слова, пишущиеся через дефис, считаются 1 словом.
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
        yield word