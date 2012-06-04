"""
Models for a project
"""

from django.core import models


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Milestone(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, related_name='milestones')

    def __unicode__(self):
        return self.name


class Bug(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, related_name='bugs')
    milestone = models.ForeignKey(Milestone, related_name='bugs',
        blank=True, null=True)

    def __unicode__(self):
        return self.name
