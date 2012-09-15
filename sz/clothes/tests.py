# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from sz.clothes.models import Tag, Pattern
from sz.clothes import services

class SimpleTest(TestCase):
    def setUp(self):
        self.patterns = [
            Pattern(tag = Tag(name = u'майка'), value = u'май'), 
            Pattern(tag = Tag(name = u'обувь'), value = u'болотник'),
            Pattern(tag = Tag(name = u'шапка'), value = u'шапк'),
            Pattern(tag = Tag(name = u'шапка'), value = u'шапочк'),
        ]
    def test_lower_case_char_field(self):
        tag = Tag(name = u'ФутБолка')
        self.assertEqual(tag.name, u'футболка')
    
    def test_taging_service(self):
        
        print '[REGEXP]'
        print services.list_debug_info(
            lambda pattern: u'{%s - %s}' % (pattern.tag, pattern), 
            self.patterns, 
            u'Шаблоны:')
        message = u'Спининги, болотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = services.regexp_tags(message, self.patterns) 
        print services.list_debug_info(lambda tag: tag, tags, u'Тэги:')
        self.assertEqual(tags, [u'обувь'])
        
    def test_taging_service_spell(self):
        print '[SPELL]'
        print services.list_debug_info(
            lambda pattern: u'{%s - %s}' % (pattern.tag, pattern), 
            self.patterns, 
            u'Шаблоны:')
        message = u'Спининги, болотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = services.regexp_tags(message, self.patterns)    
        print services.list_debug_info(lambda tag: tag, tags, u'Тэги:')
        self.assertEqual(tags, [u'обувь'])