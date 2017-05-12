from django.shortcuts import render

from django.http import HttpResponse

from index.views import isInstructor, invalidAccess

from ..models import Course
from .models import Module
from component.models import Component

import json

# Create your views here.
def index(request, course_id, module_id):
    if isInstructor(request):
        course = Course.objects.filter(id=course_id)
        module = Module.objects.filter(id=module_id, course=course_id)
        components = Component.objects.filter(module=module_id).order_by('order_no')
        if course.count() == 0 or module.count() == 0:
            return invalidAccess()
        course = course[0]
        module = module[0]
        if course.instructor.id != request.session['user_id']:
            return invalidAccess()
        output = {'course': course, 'module': module, 'components': components}
        return HttpResponse(render(request, 'course/module/index.html', output))
    return invalidAccess()

def add(request, course_id):
    if not isInstructor(request):
        return invalidAccess()
    course = Course.objects.filter(id=course_id)
    if course.count() == 0:
        return invalidAccess()
    course = course[0]
    if 'name' not in request.POST:
        output = {'course': course}
        return HttpResponse(render(request, 'course/module/add.html', output))
    if course.instructor.id != request.session['user_id']:
        return invalidAccess()
    name = request.POST['name']
    lastModule = Module.objects.filter(course=course_id).order_by('-order_no')
    order_no = lastModule.count()
    module = Module(name=name, course=course, order_no=order_no)
    module.save()
    return HttpResponse(module.id)

def save_order(request, course_id, module_id):
    if not isInstructor(request) or 'order' not in request.POST:
        return invalidAccess()
    course_id = int(course_id)
    module_id = int(module_id)
    course = Course.objects.filter(id=course_id)
    module = Module.objects.filter(id=module_id, course=course_id)
    if course.count() == 0 or module.count() == 0:
        return invalidAccess()
    course = course[0]
    module = module[0]
    if course.instructor.id != request.session['user_id']:
        return invalidAccess()
    order = json.loads(request.POST['order'])
    for val in order:
        component = Component.objects.filter(id=val)
        if component.count() == 0 or component[0].module_id != module_id:
            return invalidAcces()
    for i, val in enumerate(order):
        component = Component.objects.filter(id=val)
        component.update(order_no=i)
    return HttpResponse('success')
