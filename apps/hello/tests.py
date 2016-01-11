from django import test
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from .views import home


class HomePageTests(test.TestCase):

    def test_hardcoded_data(self):
        '''Checking presence of hardcoded data
        '''
        client = test.Client()
        response = client.get('/')
        self.assertContains(response, '42 Coffee Cups Test Assignment')

    def test_homepage_view(self):
        '''Checking presence of hardcoded data in the home view
        '''
        request = HttpRequest()
        response = home(request)
        self.assertContains(response, '42 Coffee Cups Test Assignment')


class UserModelTests(test.TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        '''Create user with additional profile fields
        '''
        user = self.User.objects.create_user(
            username='_test_user',
            password='_test_pass',
            birthday='2000-01-01')
        self.assertIsInstance(user, self.User)

    def test_admin_user_present(self):
        '''User named 'admin' exists on db creation
        '''
        user = self.User.objects.get(username='admin')
        self.assertIsInstance(user, self.User)
