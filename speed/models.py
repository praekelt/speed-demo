from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from jmbo.models import ModelBase


class TrivialContent(ModelBase):
    """We need one model so South migrations can be initiated."""
    pass


class Car(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title


class Container(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, blank=True)
    target_content_type = models.ForeignKey(ContentType, blank=False, null=True)
    target_object_id = models.PositiveIntegerField(blank=False, null=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    def __unicode__(self):
        return self.title

    @property
    def children(self):
        return Container.objects.filter(parent=self)
