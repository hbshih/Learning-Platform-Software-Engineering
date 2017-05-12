from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect

from datetime import datetime

from django.db.models import Q
from index.models import User
from .models import Category, Status, Course, EnrolledCourse
from module.models import Module, ModuleProgress
from module.component.models import Component, ComponentProgress

from index.views import isInstructor, isParticipant, invalidAccess, getEnrolledCourse

import json

# Create your views here.
def index(request, course_id):
    course = Course.objects.filter(id=course_id)
    if course.count() == 0:
        return invalidAccess()
    course = course[0]
    modules = Module.objects.filter(course=course_id).order_by('order_no')
    if isParticipant(request):
        if course.is_open == 0:
            return HttpResponse('Course is closed')
        enrolledCourse = EnrolledCourse.objects.filter(course=course_id, user=request.session['user_id'])
        if enrolledCourse.count() == 0:
            return invalidAccess()
        enrolledCourse = enrolledCourse[0]
        inProgress = Status.objects.filter(name="In Progress")[0].id
        completed = Status.objects.filter(name="Completed")[0].id
        retake = Status.objects.filter(name="Retake")[0].id
        currentStatus = enrolledCourse.status.id
        if currentStatus != inProgress and currentStatus != completed and currentStatus != retake:
            return invalidAccess()
        for i, module in enumerate(modules):
            components = Component.objects.filter(module=module).order_by('order_no')
            modules[i].components = components
            module_progress = ModuleProgress.objects.filter(enrolled_course=enrolledCourse, module=module)
            if module_progress.count() == 0:
                module_progress = ModuleProgress(enrolled_course=enrolledCourse, module=module, status=enrolledCourse.status)
                module_progress.save()
            else:
                module_progress = module_progress[0]
            modules[i].module_progress = module_progress
            if i == 0:
                modules[i].can_view = True
                if module.components.count() == 0:
                    ModuleProgress.objects.filter(id=module_progress.id).update(status=completed)
            if i < modules.count() - 1:
                modules[i + 1].can_view = False
                if module_progress.status.id == completed:
                    modules[i + 1].can_view = True
                if modules[i].can_view == True and module.components.count() == 0:
                    modules[i + 1].can_view = True
                    ModuleProgress.objects.filter(id=module_progress.id).update(status=completed)
            if i == modules.count() - 1:
                if modules[i].can_view == True and module.components.count() == 0:
                    ModuleProgress.objects.filter(id=module_progress.id).update(status=completed)
                module_progress = ModuleProgress.objects.filter(id=module_progress.id)[0]
                if module_progress.status.id == completed:
                    if enrolledCourse.status.id != completed:
                        EnrolledCourse.objects.filter(course=course_id, user=request.session['user_id']).update(status=completed, completion_date=datetime.now())
        output = {'course': course, 'modules': modules}
        output = getEnrolledCourse(request, output)
        if currentStatus == inProgress or currentStatus == retake:
            output['action'] = 'drop'
        if currentStatus == completed:
            if EnrolledCourse.objects.filter(user=request.session['user_id']).filter(Q(status__name="In Progress") | Q(status__name="Retake")).count() == 0:
                output['action'] = 'retake'
        return HttpResponse(render(request, 'course/index-participant.html', output))
    if isInstructor(request):
        if course.instructor.id != request.session['user_id']:
            return InvalidAccess()
        output = {'course': course, 'modules': modules}
        return HttpResponse(render(request, 'course/index-instructor.html', output))
    return HttpResponse('Unknown Request')

def add(request):
    if not isInstructor(request):
        return invalidAccess()
    if 'name' not in request.POST or 'category' not in request.POST or 'description' not in request.POST:
        output = {'categories': Category.objects.all()}
        return HttpResponse(render(request, 'course/add.html', output))
    name = request.POST['name']
    category = Category.objects.filter(id=request.POST['category'])[0]
    description = request.POST['description']
    instructor = User.objects.filter(id=request.session['user_id'])[0]
    course = Course(name=name, category=category, description=description, instructor=instructor, is_open=0)
    course.save()
    return HttpResponse(course.id)

def save_order(request, course_id):
    if not isInstructor(request) or 'order' not in request.POST:
        return invalidAccess()
    course_id = int(course_id)
    course = Course.objects.filter(id=course_id)
    if course.count() == 0:
        return invalidAccess()
    course = course[0]
    if course.instructor.id != request.session['user_id']:
        return invalidAccess()
    order = json.loads(request.POST['order'])
    for val in order:
        module = Module.objects.filter(id=val)
        if module.count() == 0 or module[0].course.id != course_id:
            return invalidAccess()
    for i, val in enumerate(order):
        module = Module.objects.filter(id=val)
        module.update(order_no=i)
    return HttpResponse('success')

def open(request, course_id):
    return switch_course_open_status(request, course_id, 1)

def close(request, course_id):
    return switch_course_open_status(request, course_id, 0)

def switch_course_open_status(request, course_id, is_open):
    if not isInstructor(request):
        return invalidAccess()
    course_id = int(course_id)
    course = Course.objects.filter(id=course_id)
    if course.count() == 0:
        return invalidAccess()
    if course[0].instructor.id != request.session['user_id']:
        return invalidAccess()
    course.update(is_open=is_open)
    return redirect('/course/' + str(course_id))

def overview(request, course_id):
    course = Course.objects.filter(id=course_id, is_open=1)
    if course.count() == 0:
        return invalidAccess()
    course = course[0]
    enrolledCourse = EnrolledCourse.objects.filter(course=course.id, user=request.session['user_id'])
    inProgress = Status.objects.filter(name="In Progress")[0].id
    completed = Status.objects.filter(name="Completed")[0].id
    retake = Status.objects.filter(name="Retake")[0].id
    if enrolledCourse.count() > 0:
        enrolledCourse = enrolledCourse[0]
        currentStatus = enrolledCourse.status.id
        if currentStatus == inProgress or currentStatus == retake:
            course.action = "drop"
        if currentStatus == completed:
            course.action = "retake"
    courseTaken = EnrolledCourse.objects.filter(user=request.session['user_id']).filter(Q(status=inProgress) | Q(status=retake))
    if courseTaken.count() > 0:
        course.action = "enrolled"
        course.enrolledId = courseTaken[0].course.id
    output = {'course': course}
    output = getEnrolledCourse(request, output)
    return HttpResponse(render(request, 'course/overview.html', output))

def enroll(request, course_id):
    course_id = int(course_id)
    if not isParticipant(request):
        return invalidAccess()
    inProgress = Status.objects.filter(name="In Progress")[0].id
    retake = Status.objects.filter(name="Retake")[0].id
    courseTaken = EnrolledCourse.objects.filter(user=request.session['user_id']).filter(Q(status=inProgress) | Q(status=retake))
    if courseTaken.count() > 0:
        return redirect('/course/' + str(course_id) + '/overview')
    course = Course.objects.filter(id=course_id, is_open=1)
    if course.count() == 0:
        return invalidAccess()
    course = course[0]
    enrolledCourse = EnrolledCourse.objects.filter(course=course_id, user=request.session['user_id'])
    if enrolledCourse.count() == 0:
        user = User.objects.filter(id=request.session['user_id'])[0]
        status = Status.objects.filter(name='In Progress')[0]
        enrolledCourse = EnrolledCourse(course=course, user=user, status=status)
        enrolledCourse.save()
        modules = Module.objects.filter(course=course_id)
        for module in modules:
            moduleProgress = ModuleProgress(enrolled_course=enrolledCourse, module=module, status=status)
            moduleProgress.save()
            components = Component.objects.filter(module=module.id)
            for component in components:
                componentProgress = ComponentProgress(module_progress=moduleProgress, component=component, status=status)
                componentProgress.save()
    else:
        if enrolledCourse[0].status.id != Status.objects.filter(name='Completed')[0].id and enrolledCourse[0].status.id != Status.objects.filter(name='Dropped')[0].id:
            return invalidAccess()
        status = Status.objects.filter(name='Retake')[0]
        modules = ModuleProgress.objects.filter(enrolled_course=enrolledCourse[0].id)
        modules.update(status=status)
        for module in modules:
            components = ComponentProgress.objects.filter(module_progress=module.id)
            components.update(status=status)
        enrolledCourse.update(status=status)
    return redirect('/course/' + str(course_id))

def drop(request, course_id):
    course_id = int(course_id)
    if not isParticipant(request):
        return invalidAccess()
    course = Course.objects.filter(id=course_id, is_open=1)
    if course.count() == 0:
        return invalidAccess()
    course = course[0]
    enrolledCourse = EnrolledCourse.objects.filter(course=course_id, user=request.session['user_id'])
    if enrolledCourse.count() == 0:
        return invalidAccess()
    if enrolledCourse[0].status.id == Status.objects.filter(name='Completed')[0].id:
        return invalidAccess()
    status = Status.objects.filter(name='Dropped')[0]
    modules = ModuleProgress.objects.filter(enrolled_course=enrolledCourse[0].id)
    modules.update(status=status)
    for module in modules:
        components = ComponentProgress.objects.filter(module_progress=module.id)
        components.update(status=status)
    enrolledCourse.update(status=status)
    return redirect('/course/' + str(course_id) + '/overview')
