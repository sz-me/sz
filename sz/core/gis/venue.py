# -*- coding: utf-8 -*-
from foursquare import Foursquare
from sz.settings import FOURSQUARE_CONFIG

def search(position, query, radius):
    client = Foursquare(
        client_id = FOURSQUARE_CONFIG['client_id'],
        client_secret = FOURSQUARE_CONFIG['client_secret'],
        redirect_uri = FOURSQUARE_CONFIG['redirect_uri'],
        version='20120609',
    )
    params={
        'll': ('%s,%s' % (position['latitude'], position['longitude'])),
        'categoryId': '4d4b7105d754a06378d81259',
        'limit':15,
        }
    if position.get('accuracy'):
        params['llAcc'] = position['accuracy']
    if radius:
        params['radius'] = radius
    if query:
        params['query'] = query.encode('utf8')
    response =  client.venues.search(params)
    return response
