# -*- coding: utf-8 -*-
import re
from sz.core import morphology

class ExitLoop(Exception):
    pass

class RussianStemmer:
    cacheLevel = 1
    cache = {}

    vowel = morphology.VOWEL_RU
    perfectiveground = u"((ив|ивши|ившись|ыв|ывши|ывшись)|((?<=[ая])(в|вши|вшись)))$"
    reflexive = u"(с[яь])$"
    adjective = u'(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$';
    participle = u'((ивш|ывш|ующ)|((?<=[ая])(ем|нн|вш|ющ|щ)))$';
    verb = u'((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|((?<=[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$';
    noun = u'(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$';
    rvre = u'^(.*?[аеиоуыэюя])(.*)$';
    derivational = u'[^аеиоуыэюя][аеиоуыэюя]+[^аеиоуыэюя]+[аеиоуыэюя].*(?<=о)сть?$';

    def __init__(self, cache = 1):
        pass

    def s(self, pattern, repl,  str):
        return re.sub(pattern, repl, str) == str

    def stemWord(self,  word):
        word = word.lower().replace(u'ё', u'е')

        if self.cacheLevel and word in self.cache:
            return self.cache[word]

        stem = word

        try:
            matches = re.match(self.rvre, word)
            if not matches:
                raise ExitLoop()

            start,  RV = matches.groups()

            if not RV:
                raise ExitLoop()

            # Step 1
            if self.s(self.perfectiveground, '', RV):
                RV = re.sub(self.reflexive, '', RV)

                if not self.s(self.adjective, '', RV):
                    RV = re.sub(self.adjective, '', RV)
                    RV = re.sub(self.participle, '', RV)
                else:
                    if self.s(self.verb, '', RV):
                        RV = re.sub(self.noun, '', RV)
                    else:
                        RV = re.sub(self.verb, '', RV)
            else:
                RV = re.sub(self.perfectiveground, '', RV)

            # Step 2
            RV = re.sub(u'и$', '', RV)

            # Step 3
            if re.search(self.derivational, RV):
                RV = re.sub(u'ость?$', '', RV)

            # Step 4
            if self.s(u'ь$', '', RV):
                RV = re.sub(u'ейше?', '', RV)
                RV = re.sub(u'нн$', u'н', RV)
            else:
                RV = re.sub(u'ь$', '', RV)

            stem = start + RV
        except ExitLoop:
            pass

        if self.cacheLevel:
            self.cache[word] = stem

        return stem