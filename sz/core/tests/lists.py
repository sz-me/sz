# -*- coding: utf-8 -*-
from django.test import TestCase
from sz.core import lists

class ListsTest(TestCase):
    def test_any(self):
        self.assertFalse(lists.any(lambda x: x < 0, [1, 2, 3]))
        self.assertFalse(lists.any(lambda x: x != None, [None, None, None]))
        self.assertTrue(lists.any(lambda x: x > 1, [0, 1, 2]))
    def test_all(self):
        self.assertTrue(lists.all(lambda x: x > 0, [1, 2, 3]))
        self.assertFalse(lists.all(lambda x: x == None, set([None, 1])))
        self.assertFalse(lists.all(lambda x: x > 1, [0, 1, 2]))
    def test_first(self):
        self.assertEquals(lists.first([4, 2, 3]), 4)
        self.assertEquals(lists.first(set([4, 5, 3, 'a', 18])), 'a')
    def test_last(self):
        self.assertEquals(lists.last([4, 2, 3]), 3)
    def test_first_match(self):
        self.assertEquals(lists.first_match(lambda x: x < 4, [4, 2, 3, 5]), 2)
        self.assertEquals(lists.first_match(lambda x: x < 1, [4, 2, 3, 5]), None)
    def test_last_match(self):
        self.assertEquals(lists.last_match(lambda x: x < 4, [4, 2, 3, 5]), 3)
        self.assertEquals(lists.last_match(lambda x: x > 7, [4, 2, 3, 5]), None)
