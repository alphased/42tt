from django.db import models


class Requests(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=8)
    path = models.CharField(max_length=256)

    def __unicode__(self):
        return u'%s %s' % (self.method, self.path)
