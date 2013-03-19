# -*- coding: utf-8 -*-
from math import acos, atan2, cos, pi, radians, sin
from django.contrib.gis.geos import fromstr


def ll_to_point(longitude, latitude, srid=4326):
    return fromstr('POINT(%s %s)' % (longitude, latitude), srid=4326)


# http://en.wikipedia.org/wiki/Earth_radius
# """For Earth, the mean radius is 6,371.009 km (˜3,958.761 mi; ˜3,440.069 nmi)"""
EARTH_RADIUS_IN_M = 6371009


def distance(long_a, lat_a, long_b, lat_b,):
    """all angles in degrees, result in miles"""
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    delta_long = radians(long_a - long_b)
    cos_x = (
        sin(lat_a) * sin(lat_b) +
        cos(lat_a) * cos(lat_b) * cos(delta_long)
        )
    return acos(cos_x) * EARTH_RADIUS_IN_M


def distance_p(point_a, point_b):
    return distance(point_a.x, point_a.y, point_b.x, point_b.y)


def azimuth(loc_long, loc_lat, dest_long, dest_lat):
    """ Calculates azimuth of destination point (long=λ2, lat=φ2) from location point (λ1, φ1)
    θ = atan2( sin(Δλ).cos(φ2), cos(φ1).sin(φ2) − sin(φ1).cos(φ2).cos(Δλ) ) """
    phi1 = radians(loc_lat)
    phi2 = radians(dest_lat)
    delta = radians(dest_long - loc_long)
    y = sin(delta) * cos(phi2)
    x = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(delta)
    azimuth_in_radians = atan2(y, x)
    # az_deg = ( az_rad * 180 / pi + 360 ) % 360
    azimuth_in_degrees = (azimuth_in_radians * 180 / pi + 360) % 360
    return azimuth_in_degrees
