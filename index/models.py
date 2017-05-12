from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=4096)
    name = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    def __str__(self):
        return self.username
