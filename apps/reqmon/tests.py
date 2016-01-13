from django.test import Client, TestCase
from django.core.urlresolvers import reverse
import beautifulsoupselect as bss


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
