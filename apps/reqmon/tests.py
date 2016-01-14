from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from reqmon.models import Requests
import beautifulsoupselect as bss
import json


class RequestsModelTests(TestCase):

    def test_model_fields(self):
        '''Model stores all required data (timestamp, path, method)
        '''
        user = Requests.objects.create(
            method='GET',
            path='/')
        self.assertTrue(user.timestamp)


class RequestsMiddlewareTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.link_requests = reverse('requests')

    def test_middleware_got_requests(self):
        '''Middleware stores requests which got a corresponding view
        '''
        self.client.get(self.link_requests)
        self.assertEquals(self.link_requests, Requests.objects.get(pk=1).path)


class RequestsPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.link_home = reverse('home')
        self.link_requests = reverse('requests')
        self.link_requests_updates = reverse('requests_updates')

    def test_home_link(self):
        '''Page contains the link to the 'home' page
        '''
        response = self.client.get(self.link_requests)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertTrue(soup('a[href="%s"]' % self.link_home))

    def test_amount_ordering(self):
        '''View contains no more than last 10 requests and has the proper ordering
        '''
        for _ in range(10):
            self.client.head(self.link_home)
        response = self.client.get(self.link_requests)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertEquals(10, len(soup('ul#requests li')))
        self.assertIn(self.link_requests, soup('ul#requests li')[0].text)

    def test_form_contains(self):
        '''view form contains latest request_id
        '''
        response = self.client.get(self.link_requests)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertEquals(
            1,
            int(soup('form#requests_form input[name=last]')[0]['value']))

    def test_ajax_request(self):
        '''Ajax endpoint returns results for zero, one and multiple requests
        '''

        def do_request(last):
            return self.client.get(self.link_requests_updates, {'last': last},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                   follow=False)

        # First call returns no new requests; status code and 'OK' tested
        response = do_request(1)
        result = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals('OK', result['result'])
        self.assertEquals(0, len(result['requests']))
        self.assertEquals(1, result['latest'])

        # Second call returns one request
        response = do_request(1)
        result = json.loads(response.content)
        self.assertEquals(1, len(result['requests']))
        self.assertEquals(2, result['latest'])

        # Third call returns two requests
        response = do_request(1)
        result = json.loads(response.content)
        self.assertEquals(2, len(result['requests']))
        self.assertEquals(3, result['latest'])

        #  Check getting ERROR and 400 status on malformed parameter
        response = do_request('')
        result = json.loads(response.content)
        self.assertEquals(400, response.status_code)
        self.assertEquals('ERROR', result['result'])

        response = do_request('-1')
        result = json.loads(response.content)
        self.assertEquals(400, response.status_code)

        response = do_request(' duh')
        result = json.loads(response.content)
        self.assertEquals(400, response.status_code)

        # Check this out, we got them all (it's a feature :)
        response = do_request(0)
        result = json.loads(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(7, len(result['requests']))
        self.assertEquals(7, result['latest'])
