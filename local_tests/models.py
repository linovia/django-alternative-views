
from django.db import models


class MyObjectModel(models.Model):
    slug = models.CharField(max_length=8)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return u'%i' % (self.id,)


class MyOtherObjectModel(models.Model):
    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return u'%i' % (self.id,)
