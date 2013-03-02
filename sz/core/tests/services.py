from django.test import TestCase
from sz.core.services import parameters
from sz.core.services import gis


class DecoratorsTest(TestCase):

    def test_location_decorator(self):
        params1 = dict(
            latitude=50.2616113,
            longitude=127.5266082
        )
        params2 = dict(
            latitude=50.2616113,
            longitude=127.5266082,
            radius=-300
        )
        
        dec1 = parameters.LocationDecorator(params1, gis.BlagoveshchenskCityService())
        self.assertDictEqual(
            dec1.get_api_params(),
            {'latitude': 50.2616113, 'longitude': 127.5266082}
        )
        self.assertDictEqual(
            dec1.get_db_params(),
            {'latitude': 50.2616113, 'radius': None, 'longitude': 127.5266082, 'city_id': 2026609}
        )

        dec2 = parameters.LocationDecorator(params2, gis.BlagoveshchenskCityService())
        self.assertDictEqual(
            dec2.get_api_params(),
            {'latitude': 50.2616113, 'longitude': 127.5266082}
        )
        self.assertDictEqual(
            dec2.get_db_params(),
            {'latitude': 50.2616113, 'radius': None, 'longitude': 127.5266082, 'city_id': 2026609}
        )

    def test_paging_decorator(self):
        params1 = {'max_id': 5}
        params2 = {'max_id': -10}
        positionDecorator1 = parameters.PagingDecorator(params1, 300, 17)
        positionDecorator2 = parameters.PagingDecorator(params2, 300, 17)
        self.assertDictEqual(
            positionDecorator1.get_api_params(),
            {'limit': 17, 'max_id': 5, 'offset': 0}
        )
        self.assertDictEqual(
            positionDecorator1.get_db_params(),
            {'limit': 17, 'max_id': 5, 'offset': 0}
        )
        self.assertDictEqual(
            positionDecorator2.get_api_params(),
            {'limit': 17, 'max_id': 300, 'offset': 0}
        )
        self.assertDictEqual(
            positionDecorator2.get_db_params(),
            {'limit': 17, 'max_id': 300, 'offset': 0}
        )