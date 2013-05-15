import hashlib
import random

from django.test import TestCase

from sz.core.services import parameters
from sz.core.services import gis
from sz.core.services.email import EmailService


class CategorizationServiceMock:
    def detect_stems(self):
        return set([])

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

    def test_content_decorator(self):
        params1 = {'photo': True}
        params2 = {'photo': False}
        categorizationService = CategorizationServiceMock()
        contentDecorator1 = parameters.ContentDecorator(params1, categorizationService)
        contentDecorator2 = parameters.ContentDecorator(params2, categorizationService)
        print contentDecorator2.get_api_params()
        self.assertDictEqual(
            contentDecorator1.get_api_params(),
            {'category': None, 'photo': True}
        )
        self.assertDictEqual(
            contentDecorator1.get_db_params(),
            {'category': None, 'photo': True, 'stems': []}
        )
        self.assertDictEqual(
            contentDecorator2.get_api_params(),
            {'category': None}
        )
        self.assertDictEqual(
            contentDecorator2.get_db_params(),
            {'category': None, 'photo': None, 'stems': []}
        )


def send_mail_mock(subject, message, from_email, recipient_list):
    return {
        'subject': subject,
        'message': message,
    }


class EmailServiceTest(TestCase):

    def test_template_message(self):
        service = EmailService()
        service.send_mail = send_mail_mock
        confirmation_key = hashlib.md5(str(random.random())).hexdigest()
        site = 'shmotzhmot.me'
        email = service.send_template_message(
            'registration/confirmation_email_subject.txt',
            'registration/confirmation_email_message.txt',
            {
                'confirmation_key': confirmation_key,
                'site': site
            },
            None
        )
        self.assertIn(confirmation_key, email['message'])
        self.assertIn(site, email['subject'])
