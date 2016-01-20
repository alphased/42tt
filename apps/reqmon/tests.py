from django.test import Client, TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from reqmon.models import Requests
import beautifulsoupselect as bss
import json


# Requests middleware test settings defaults
requests_middleware_defaults = {
    'SKIP_PATH': [reverse('requests_updates'), ],
    'PRI1_PATH': [reverse('admin:index'), ],
}


class RequestsModelTests(TestCase):

    def test_model_fields(self):
        '''Model stores all required data (timestamp, path, method)
        '''
        request = Requests.objects.create(method='GET', path='/')
        self.assertTrue(request.timestamp)


class RequestsMiddlewareTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.link_home = reverse('home')
        self.link_admin = reverse('admin:index')
        self.link_requests = reverse('requests')

    def test_middleware_got_requests(self):
        '''Middleware stores requests which got a corresponding view
        '''
        self.client.get(self.link_requests)
        self.assertEquals(self.link_requests, Requests.objects.get(pk=1).path)

    @override_settings(**requests_middleware_defaults)
    def test_middleware_priority0_home(self):
        '''Middleware set priority 0 for request to home
        '''
        self.client.get(self.link_home)
        self.assertEquals(0, Requests.objects.get(pk=1).priority)

    @override_settings(**requests_middleware_defaults)
    def test_middleware_priority1_admin(self):
        '''Middleware set priority 1 for request to admin
        '''
        self.client.get(self.link_admin)
        self.assertEquals(1, Requests.objects.get(pk=1).priority)

    def test_middleware_priority1_post(self):
        '''Middleware set priority 1 for POST requests
        '''
        self.client.post(self.link_requests)
        self.assertEquals(1, Requests.objects.get(pk=1).priority)


class RequestsPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.link_home = reverse('home')
        self.link_admin = reverse('admin:index')
        self.link_requests = reverse('requests')

    def test_home_link(self):
        '''Page contains the link to the 'home' page
        '''
        response = self.client.get(self.link_requests)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertTrue(soup('a[href="%s"]' % self.link_home))

    def test_amount_ordering_reverse(self):
        '''View contains no more than last 10 requests and has the proper ordering
           (all params by default: reverse=1, priority=0)
        '''
        for _ in range(10):
            self.client.head(self.link_home)
        response = self.client.get(self.link_requests)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertEquals(10, len(soup('ul#requests li')))
        self.assertIn(self.link_requests, soup('ul#requests li')[0].text)

    def test_amount_ordering_chronological(self):
        '''View contains no more than last 10 requests and has the proper ordering
           (all params by default: reverse=0, priority=1)
        '''
        for _ in range(10):
            self.client.post(self.link_requests)
        response = self.client.get(self.link_admin)
        response = self.client.get(self.link_requests,
                                   {'priority': 1, 'reverse': 0})
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertEquals(10, len(soup('ul#requests li')))
        self.assertIn(self.link_requests,
                      soup('ul#requests li')[8].text)
        self.assertIn(self.link_admin,
                      soup('ul#requests li')[9].text)

    def test_form_contains(self):
        '''view form contains latest request_id
        '''
        response = self.client.get(self.link_requests)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertEquals(200, response.status_code)
        self.assertEquals(
            1,
            int(soup('form#requests_form input#last')[0]['value']))


class RequestsUpdatesTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.link_requests = reverse('requests')
        self.link_requests_updates = reverse('requests_updates')

    def test_ajax_request(self):
        '''Ajax endpoint returns results for zero, one and multiple requests
        '''

        def do_request(last, priority=0):
            self.client.get(self.link_requests)
            response = self.client.get(self.link_requests_updates,
                                       {'last': last, 'priority': priority},
                                       HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                       follow=False)
            result = json.loads(response.content)
            return response, result

        # First call returns one request; status code and 'OK' tested
        response, result = do_request(0)
        self.assertEquals(200, response.status_code)
        self.assertEquals('OK', result['result'])
        self.assertEquals(1, len(result['requests']))
        self.assertEquals(1, result['latest'])

        # Second call returns one request
        response, result = do_request(1)
        self.assertEquals(1, len(result['requests']))
        self.assertEquals(2, result['latest'])

        # Third call returns two requests
        response, result = do_request(1)
        self.assertEquals(2, len(result['requests']))
        self.assertEquals(3, result['latest'])

        #  Check getting ERROR and 400 status on malformed parameter
        response, result = do_request('')
        self.assertEquals(400, response.status_code)
        self.assertEquals('ERROR', result['result'])

        response, result = do_request('-1')
        self.assertEquals(400, response.status_code)

        response, result = do_request(' duh')
        self.assertEquals(400, response.status_code)

        # Check this out, we got them all
        response, result = do_request(0)
        self.assertEquals(200, response.status_code)
        self.assertEquals(7, len(result['requests']))
        self.assertEquals(7, result['latest'])

        # Got one request with priority 1
        self.client.post(self.link_requests)
        response, result = do_request(0, 1)
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, len(result['requests']))
        self.assertEquals(8, result['latest'])

        # Here goes second
        self.client.post(self.link_requests)
        response, result = do_request(0, 1)
        self.assertEquals(2, len(result['requests']))
        self.assertEquals(10, result['latest'])
