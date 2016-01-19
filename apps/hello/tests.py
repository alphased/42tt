from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
import beautifulsoupselect as bss


class UserModelTests(TestCase):

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


class HomePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.link_home = reverse('home')
        self.link_requests = reverse('requests')

    def test_hardcoded_data(self):
        '''Checking presence of hardcoded data
        '''
        response = self.client.get(self.link_home)
        self.assertContains(response, 'Enough is enough')

    def test_no_user(self):
        '''Page contains hard-coded data in case of no users in DB
        '''
        self.User.objects.all().delete()
        response = self.client.get(self.link_home)
        self.assertContains(response, 'Enough is enough')

    def test_more_than_one_user(self):
        '''Page still contains 'admin' user data in case of more than one user in DB
        '''
        self.User.objects.create_user(username='adminna')
        response = self.client.get(self.link_home)
        self.assertContains(response, 'Enough is enough')

    def test_requests_link(self):
        '''Page contains the link to the 'requests' page
        '''
        response = self.client.get(self.link_home)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertTrue(soup('a[href="%s"]' % self.link_requests))
