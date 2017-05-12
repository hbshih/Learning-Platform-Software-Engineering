from __future__ import unicode_literals

from django.db import models

from course.models import Course, EnrolledCourse, Status

# Create your models here.
class Module(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order_no = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.name

class ModuleProgress(models.Model):
    enrolled_course = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
