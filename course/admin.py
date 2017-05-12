from django.contrib import admin

from .models import Category, Status, Course, EnrolledCourse
from .module.models import Module, ModuleProgress
from .module.component.models import ComponentType, Component, Text, Image, File, Quiz

# Register your models here.
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Course)
admin.site.register(EnrolledCourse)
admin.site.register(Module)
admin.site.register(ModuleProgress)
admin.site.register(ComponentType)
admin.site.register(Component)
admin.site.register(Text)
admin.site.register(Image)
admin.site.register(File)
admin.site.register(Quiz)
