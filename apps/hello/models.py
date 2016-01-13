from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    contact_jabber = models.CharField(max_length=30, blank=True)
    contact_skype = models.CharField(max_length=30, blank=True)
    othercontacts = models.TextField(blank=True)
    bio = models.TextField(blank=True)
