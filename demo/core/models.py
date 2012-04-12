from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Milestone(models.Model):
    name = models.CharField(max_length=64)
    project = models.ForeignKey(Project, related_name='milestones')
    active = models.BooleanField()
    finished = models.BooleanField()

    def __unicode__(self):
        return self.name
