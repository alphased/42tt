from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from reqmon.models import Requests
import beautifulsoupselect as bss


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


class ResuestsPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.link_home = reverse('home')
        self.link_requests = reverse('requests')

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
