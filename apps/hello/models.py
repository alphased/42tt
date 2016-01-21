from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    contact_jabber = models.CharField(max_length=30, blank=True)
    contact_skype = models.CharField(max_length=30, blank=True)
    othercontacts = models.TextField(blank=True)
    bio = models.TextField(blank=True)


class Event(models.Model):

    action_time = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"
        ordering = ('-action_time',)
