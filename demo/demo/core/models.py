"""
Models for a project
"""

from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    members = models.ManyToManyField('auth.User', related_name='projects')

    def __unicode__(self):
        return self.name


class Milestone(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, related_name='milestones')

    def __unicode__(self):
        return self.name


BUG_STATUS = (
    ('new', 'New'),
    ('open', 'Open'),
    ('closed', 'Closed'),
)


class Bug(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, related_name='bugs')
    milestone = models.ForeignKey(Milestone, related_name='bugs',
        blank=True, null=True)
    status = models.CharField(max_length=32, default='new')

    def __unicode__(self):
        return self.name
