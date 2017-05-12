from __future__ import unicode_literals

from django.db import models

from index.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_open = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.name

class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(null=True)
