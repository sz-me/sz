"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import string
from django.test import TestCase
from sz.core.algorithms import lists
from sz.core.algorithms.tagging import *

class ListsTest(TestCase):
    def test_any(self):
        self.assertFalse(lists.any(lambda x: x < 0, [1, 2, 3]))
        self.assertFalse(lists.any(lambda x: x != None, [None, None, None]))
        self.assertTrue(lists.any(lambda x: x > 1, [0, 1, 2]))

class TagsServicesTest(TestCase):
    def setUp(self):
        print u'[SETUP]'
        self.tags = { 
            u'майка': [u'май'], 
            u'обувь':[u'болотник'], 
            u'шапка':[u'шапк', u'шапочк'] }
    def print_tags(self):
        
        print lists.debug_info(
            lambda (tag, patterns): u'#%s (%s)' % (tag, string.joinfields([tag] + patterns, ',')), 
            self.tags.items(), 
            u'Словарь:'
            )
    def test_regexp(self):
        print '[REGEXP]'
        self.print_tags()
        message = u'Спининги, болотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = regexp_tagging_algorithm(message, self.tags) 
        print u'Тэги: ' + string.joinfields(tags, ', ')
        self.assertEqual(tags, [u'обувь'])
    
    def test_spellcorrector(self):
        print '[SPELL]'
        self.print_tags()
        message = u'Спининги, балотники и червячки! 15 сентября на открытии магазина Рыбалка+! Поймай скидочку!!!'
        print u'Сообщение: ' + message
        tags = spellcorrector_tagging_algorithm(message, self.tags) 
        print u'Тэги: ' + string.joinfields(tags, ', ')
        self.assertEqual(tags, [u'обувь'])
        
        