# -*- coding: utf-8 -*-
from django.contrib.gis.geos import fromstr
def ll_to_point(longitude, latitude, srid=4326):
    return fromstr('POINT(%s %s)' % (longitude, latitude), srid=4326)

from math import sin, cos, radians, acos

# http://en.wikipedia.org/wiki/Earth_radius
# """For Earth, the mean radius is 6,371.009 km (˜3,958.761 mi; ˜3,440.069 nmi)"""
EARTH_RADIUS_IN_M = 6371009

def calculate_distance(long_a, lat_a, long_b, lat_b,):
    """all angles in degrees, result in miles"""
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    delta_long = radians(long_a - long_b)
    cos_x = (
        sin(lat_a) * sin(lat_b) +
        cos(lat_a) * cos(lat_b) * cos(delta_long)
        )
    return acos(cos_x) * EARTH_RADIUS_IN_M

def calculate_distance_p(point_a, point_b):
    return calculate_distance(point_a.x, point_a.y, point_b.x, point_b.y)
