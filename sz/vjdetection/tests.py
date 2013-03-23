"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import random
import numpy as np
from django.test import TestCase
from sz.vjdetection import math as d_math


class MathTest(TestCase):

    def setUp(self):
        width = random.randint(240, 1920)
        height = random.randint(320, 1080)
        size = width * height * 3
        buffer = np.arange(size)
        self.image = buffer.reshape(width, height, 3)

    def test_validate_shape(self):
        self.assertRaises(TypeError, d_math.validate_shape, 1)
        self.assertRaises(ValueError, d_math.validate_shape, np.arange(10).reshape(2, 5))
        self.assertRaises(ValueError, d_math.validate_shape, np.arange(18).reshape(3, 3, 2))

    def test_calc_resizing_factor(self):
        max_length = 512
        factor = d_math.resizing_factor(self.image, max_length)
        print self.image.shape
        print factor
        self.assertLessEqual(self.image.shape[0] * factor, max_length)
        self.assertLessEqual(self.image.shape[1] * factor, max_length)
