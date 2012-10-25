# -*- coding: utf-8 -*-
from foursquare import Foursquare
from sz.settings import FOURSQUARE_CONFIG

def search(position, query):
    client = Foursquare(
        client_id = FOURSQUARE_CONFIG['client_id'],
        client_secret = FOURSQUARE_CONFIG['client_secret'],
        redirect_uri = FOURSQUARE_CONFIG['redirect_uri']
    )
    #print client.Venues('').search(params={'ll':'44.3,37.2', 'llAcc':'10000.0'})
    #categories = client.venues.categories()
    #categories = filter(lambda c: find(c[u'icon'][u'prefix'], u'shop') > -1, categories[u'categories'])
    #print categories #u','.join(map(lambda c: c[u'id'], categories))
    params={
        'll': ('%s,%s' % (position['latitude'], position['longitude'])),
        #'llAcc': '300000.0',
        #'radius': '%s' % (200.0 + position['accuracy']),
        'categoryId': '4d4b7105d754a06378d81259',
        'limit':15,

        }
    if query:
        params['query'] = query.encode('utf8')
    result =  client.venues.search(params)
    print result
    return result
