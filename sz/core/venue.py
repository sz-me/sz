# -*- coding: utf-8 -*-
from foursquare import Foursquare
import sz
from string import find

def search(position):
    client = Foursquare(
        client_id = sz.FOURSQUARE_CONFIG['client_id'],
        client_secret = sz.FOURSQUARE_CONFIG['client_secret'],
        redirect_uri = sz.FOURSQUARE_CONFIG['redirect_uri']
    )
    #print client.Venues('').search(params={'ll':'44.3,37.2', 'llAcc':'10000.0'})
    #categories = client.venues.categories()
    #categories = filter(lambda c: find(c[u'icon'][u'prefix'], u'shop') > -1, categories[u'categories'])
    #print categories #u','.join(map(lambda c: c[u'id'], categories))
    result =  client.venues.search(params={
        'll': ('%s,%s' % (position['latitude'], position['longitude'])),
        #'llAcc': '300000.0',
        'radius': '500.0',
        'categoryId': '4d4b7105d754a06378d81259',
        'limit':50,
        #'query': 'Остин'
    })
    return result
