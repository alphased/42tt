from django.test import Client, TestCase
from django.core import management
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context
from .models import Event, ADDITION, CHANGE, DELETION

import beautifulsoupselect as bss
from StringIO import StringIO


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
        '''Link to auth group
        '''
        group = Group.objects.create(name='linkme')
        context = Context({'object': group})
        rendered = self.template.render(context)
        self.assertIn(self.link_auth_group, rendered)


class EnumModelCommandTests(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.stdout = StringIO()
        self.stderr = StringIO()

    def test_command(self):
        '''Command output contains our user model and only initial user
        '''
        outstr = '%s.%s %d' % (self.User.__module__, self.User.__name__, 1)
        errstr = 'error: %s' % outstr
        management.call_command('enummodel',
                                stdout=self.stdout, stderr=self.stderr)
        self.assertIn(outstr, self.stdout.getvalue())
        self.assertIn(errstr, self.stderr.getvalue())


class SignalRecieverTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.instance = User.objects.create_user(username='beep_unique_user')
        content_type_id = ContentType.objects.get_for_model(self.instance).pk
        object_id = self.instance.pk
        self.filter = {'content_type_id__exact': content_type_id,
                       'object_id__exact': object_id}

    def test_model_created(self):
        '''Object already created, find it
        '''
        self.filter.update({'action_flag__exact': ADDITION})
        self.assertEquals(1, Event.objects.filter(**self.filter).count())

    def test_model_changed(self):
        '''Found one, lets chenge it
        '''
        self.instance.save()
        self.filter.update({'action_flag__exact': CHANGE})
        self.assertEquals(1, Event.objects.filter(**self.filter).count())

    def test_model_deleted(self):
        '''I'm done trash it
        '''
        self.instance.delete()
        self.filter.update({'action_flag__exact': DELETION})
        self.assertEquals(1, Event.objects.filter(**self.filter).count())


class NoSignalTests(TestCase):

    def setUp(self):
        content_type_id = ContentType.objects.get_for_model(Event).pk
        self.instance = Event.objects.log_event(
            content_type_id=content_type_id,
            object_id='', object_repr='', action_flag=0)
        object_id = self.instance.pk
        self.filter = {'content_type_id__exact': content_type_id,
                       'object_id__exact': object_id}

    def test_signal_lost(self):
        '''And silence was an answer
        '''
        self.filter.update({'action_flag__exact': ADDITION})
        self.assertEquals(0, Event.objects.filter(**self.filter).count())

        self.instance.save()
        self.filter.update({'action_flag__exact': CHANGE})
        self.assertEquals(0, Event.objects.filter(**self.filter).count())

        self.instance.delete()
        self.filter.update({'action_flag__exact': DELETION})
        self.assertEquals(0, Event.objects.filter(**self.filter).count())
