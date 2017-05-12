from __future__ import unicode_literals

from django.db import models

from embed_video.fields import EmbedVideoField

from ..models import Module
from course.models import Status
from course.module.models import ModuleProgress

import os

# Create your models here.
class ComponentType(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(max_length=1024)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type = models.ForeignKey(ComponentType, on_delete=models.CASCADE)
    order_no = models.PositiveSmallIntegerField()
    reference = models.IntegerField()
    def __str__(self):
        return self.name

class ComponentProgress(models.Model):
    module_progress = models.ForeignKey(ModuleProgress, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

class Text(models.Model):
    contents = models.TextField()
    def __str__(self):
        return str(self.id)

class Image(models.Model):
    contents = models.ImageField(upload_to="images/%Y/%m/%d")
    def __str__(self):
        return str(self.id)
    def url(self):
        return self.contents.url
    def name(self):
        return os.path.basename(self.contents.name)

class File(models.Model):
    contents = models.FileField(upload_to="files/%Y/%m/%d")
    def __str__(self):
        return str(self.id)
    def url(self):
        return self.contents.name
    def name(self):
        return os.path.basename(self.contents.name)

class Quiz(models.Model):
    quiz_id = models.IntegerField()
    question_no = models.PositiveSmallIntegerField()
    question = models.CharField(max_length=4096)
    answer = models.CharField(max_length=4096)
    def __str__(self):
        return str(self.id)

class Youtube(models.Model):
    video = EmbedVideoField()
    def __str__(self):
        return str(self.id)
