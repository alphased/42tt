from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text, force_text


class User(AbstractUser):

    birthday = models.DateField(blank=True, null=True)
    contact_jabber = models.CharField(max_length=30, blank=True)
    contact_skype = models.CharField(max_length=30, blank=True)
    othercontacts = models.TextField(blank=True)
    bio = models.TextField(blank=True)


ADDITION = 1
CHANGE = 2
DELETION = 3


class EventManager(models.Manager):

    def log_event(self, content_type_id, object_id, object_repr, action_flag):
        e = self.model(None, None, content_type_id, smart_text(object_id),
                       object_repr[:200], action_flag)
        e.save()
        return e


@python_2_unicode_compatible
class Event(models.Model):

    action_time = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()

    objects = EventManager()

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"
        ordering = ('-action_time',)

    def __repr__(self):
        return smart_text(self.action_time)

    def __str__(self):
        if self.action_flag == ADDITION:
            return 'Added %s' % self.object_repr
        elif self.action_flag == CHANGE:
            return 'Changed %s' % self.object_repr
        elif self.action_flag == DELETION:
            return 'Deleted %s' % self.object_repr
        return 'Event'

    def get_edited_object(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)


@receiver(post_save, dispatch_uid='hello.models')
def model_post_save(sender, instance, created, **kwargs):
    if sender is Event:
        return
    if created:
        Event.objects.log_event(
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=force_text(instance),
            action_flag=ADDITION)
    else:
        Event.objects.log_event(
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=force_text(instance),
            action_flag=CHANGE)


@receiver(post_delete, dispatch_uid='hello.models')
def model_post_delete(sender, instance, **kwargs):
    if sender is Event:
        return
    Event.objects.log_event(
        content_type_id=ContentType.objects.get_for_model(instance).pk,
        object_id=instance.pk,
        object_repr=force_text(instance),
        action_flag=DELETION)
