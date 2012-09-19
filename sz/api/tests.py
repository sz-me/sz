# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from sz.core.models import Tag, Pattern
from sz.api import services
from sz.core.algorithms import lists
import string

class SimpleTest(TestCase):
    def setUp(self):
        print u'[SETUP]'
        self.tags = [
            Tag(name = u'майка'),
            Tag(name = u'обувь'),
            Tag(name = u'шапка')]
        map(lambda tag: tag.save(), self.tags)
        
        self.tags[0].pattern_set.create(value = u'май')
        self.tags[1].pattern_set.create(value = u'болотник')
        self.tags[2].pattern_set.create(value = u'шапк')
        self.tags[2].pattern_set.create(value = u'шапочк')
        

    def print_tags(self):
        print lists.debug_info(
            lambda tag: u'#%s (%s)' % (tag.name, string.joinfields(map(lambda p: p.value, tag.pattern_set.all()), ',')), 
            self.tags, 
            u'Словарь:'
            )
        
    def test_lower_case_char_field(self):
        tag = Tag(name = u'ФутБолка')
        self.assertEqual(tag.name, u'футболка')
        
    def test_tags2dict(self):
        dict = services.tags2dict(self.tags)
        self.assertEqual(
            dict, 
            {
                u'майка': [u'май'], 
                u'обувь':[u'болотник'], 
                u'шапка':[u'шапк', u'шапочк'] 
            })
    
    def test_regexp_tagging_service(self):
        print '[REGEXP]'
        self.print_tags()
        message = u'Спининги, болотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = services.regexp_tagging_service(message, self.tags)
        print u'Тэги: ' + string.joinfields(tags, ', ')
        self.assertEqual(tags, [u'обувь'])
   
    def test_spell_tagging_service(self):
        print '[SPELL]'
        self.print_tags()
        message = u'Спининги, балотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = services.spellcorrector_tagging_service(message, self.tags)
        print u'Тэги: ' + string.joinfields(tags, ', ') 
        self.assertEqual(tags, [u'обувь'])

    