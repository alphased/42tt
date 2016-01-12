from django import test
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


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


class HomePageTests(test.TestCase):

    def test_hardcoded_data(self):
        '''Checking presence of hardcoded data
        '''
        client = test.Client()
        response = client.get(reverse('home'))
        self.assertContains(response, 'Enough is enough')
