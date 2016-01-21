from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.template import Template, Context
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


class EditLinkTagTests(TestCase):

    def setUp(self):
        self.link_home = reverse('home')
        self.link_admin_user = reverse('admin:hello_user_change', args=(1,))
        self.link_auth_group = reverse('admin:auth_group_change', args=(1,))
        self.template = Template("{% load edit_link %}{% edit_link object %}")

    def test_edit_link_admin(self):
        '''Page contains the link to the initial user in admin
        '''
        response = self.client.get(self.link_home)
        soup = bss.BeautifulSoupSelect(response.content)
        self.assertTrue(soup('a[href="%s"]' % self.link_admin_user))

    def test_edit_link_auth_group(self):
        group = Group.objects.create(name='linkme')
        context = Context({'object': group})
        rendered = self.template.render(context)
        self.assertIn(self.link_auth_group, rendered)

