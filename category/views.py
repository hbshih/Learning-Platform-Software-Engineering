from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect

from course.models import Category, Status, Course, EnrolledCourse
from index.models import Role
from index.views import isAdministrator, isParticipant, invalidAccess, getPage, getEnrolledCourse

import math

# Create your views here.
def index(request, category_id):
    if not isParticipant(request):
        return invalidAccess()
    category = Category.objects.filter(id=category_id)
    if category.count() == 0:
        return invalidAccess()
    category = category[0]
    ipp = 10
    page = getPage(request)
    allCourses = Course.objects.filter(category=category_id, is_open=1)
    courses = allCourses.order_by('-id')[(page - 1) * ipp:page * ipp]
    totalPages = int(math.ceil(float(allCourses.count()) / float(ipp)))
    for i, course in enumerate(courses):
        enrolledCourse = EnrolledCourse.objects.filter(course=course.id, user=request.session['user_id'])
        if enrolledCourse.count() > 0:
            enrolledCourse = enrolledCourse[0]
            currentStatus = enrolledCourse.status.name
            if currentStatus == "In Progress" or currentStatus == "Completed" or currentStatus == "Retake":
                courses[i].enrolled = True
    output = {'category': category, 'courses': courses, 'page': page, 'totalPages': totalPages}
    output = getEnrolledCourse(request, output)
    return HttpResponse(render(request, 'category/index.html', output))

def list(request):
    if not isAdministrator(request):
        return invalidAccess()
    output = {'categories': Category.objects.all().order_by('name')}
    return HttpResponse(render(request, 'category/list.html', output))

def add(request):
    if not isAdministrator(request):
        return invalidAccess()
    if 'name' not in request.POST:
        return HttpResponse(render(request, 'category/add.html'))
    else:
        name = request.POST['name']
        cat = Category(name=name)
        cat.save()
        return redirect('/category/list')

def delete(request, category_id):
    if not isAdministrator(request):
        return invalidAccess()
    cat = Category.objects.filter(id=category_id)
    if cat.count() > 0:
        cat[0].delete()
    return redirect('/category/list')

def edit(request, category_id):
    if not isAdministrator(request):
        return invalidAccess()
    if 'name' not in request.POST:
        cat = Category.objects.filter(id=category_id)
        if cat.count() > 0:
            output = {'id': cat[0].id, 'name': cat[0].name}
            return HttpResponse(render(request, 'category/edit.html', output))
        return redirect('/category/list')
    else:
        id = category_id
        name = request.POST['name']
        cat = Category.objects.filter(id=id)
        if cat.count() > 0:
            cat.update(name=name)
        return redirect('/category/list')
