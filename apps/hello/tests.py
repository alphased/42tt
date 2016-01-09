from django.test import TestCase, Client
from django.http import HttpRequest
from .views import home


class HomePageTests(TestCase):

    def test_hardcoded_data(self):
        '''Checking presence of hardcoded data
        '''
        client = Client()
        response = client.get('/')
        self.assertContains(response, '42 Coffee Cups Test Assignment')

    def test_homepage_view(self):
        '''Checking presence of hardcoded data in the home view
        '''
        request = HttpRequest()
        response = home(request)
        self.assertContains(response, '42 Coffee Cups Test Assignment')
