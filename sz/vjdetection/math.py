import math
import numpy as np


def validate_shape(value):
    if not isinstance(value, np.ndarray):
        raise TypeError('image must be a ndarray')
    if value.ndim != 3:
        raise ValueError('image must have 3 axis')
    if value.shape[2] != 3:
        raise ValueError('image must have shape (width, height, 3)')
    return True


def resizing_factor(image, max_length):
        validate_shape(image)
        length0, length1 = image.shape[:2]
        length = length1 and length1 > length0 or length0
        if length > max_length:
            return float(max_length) / float(length)
        else:
            return 1.0


# c2 > c1
def circles_ratio(c1, c2):
    x1, y1, r1 = tuple(c1)
    x2, y2, r2 = tuple(c2)
    l = math.sqrt((x1 - x2) ^ 2 - (y1 - y2) ^ 2)
    return l / r2, r1 / r2
