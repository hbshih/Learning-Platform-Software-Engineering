from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password, make_password

from urllib import urlencode

import math, re

from django.db.models import Q
from .models import Role, User
from course.models import Category, Status, Course, EnrolledCourse
from course.module.models import ModuleProgress
from course.module.component.models import ComponentProgress

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return login(request)
    user_id = request.session['user_id']
    username = request.session['username']
    role_id = request.session['role_id']
    def get_index(argument, request):
        switcher = {
            Role.objects.filter(name="Administrator")[0].id: administrator_index,
            Role.objects.filter(name="Human Resources Department")[0].id: human_resources_department_index,
            Role.objects.filter(name="Instructor")[0].id: instructor_index,
            Role.objects.filter(name="Participant")[0].id: participant_index,
        }
        return switcher.get(argument)(request)
    return get_index(role_id, request)

def login(request):
    if 'username' not in request.POST or 'password' not in request.POST:
        return HttpResponse(render(request, 'index/login.html'))
    else:
        username = request.POST['username']
        password = request.POST['password']
        as_participant = bool(request.POST.get('as_participant', False))
        user = User.objects.filter(username=username)
        if user.count() > 0 and check_password(password, user[0].password):
            request.session['user_id'] = user[0].id
            request.session['username'] = username
            request.session['role_id'] = user[0].role.id
            role = request.session['role_id']
            if Role.objects.filter(id=role, name="Instructor").count() > 0 and as_participant == True:
                request.session['role_id'] = Role.objects.filter(name="Participant")[0].id
            return redirect('/')
        else:
            output = {'errorMessage': 'Username or Password incorrect'}
            return HttpResponse(render(request, 'index/login.html', output))

def logout(request):
    del request.session['user_id']
    del request.session['username']
    del request.session['role_id']
    return redirect('/')

def register(request):
    if 'username' not in request.POST or 'password' not in request.POST or 'confirm-password' not in request.POST or 'name' not in request.POST:
        return HttpResponse(render(request, 'index/register.html'))
    else:
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirm-password']
        name = request.POST['name']
        if len(username) != 8 or not re.match("^[A-Za-z0-9_-]+$", username):
            output = {'error': 'Invalid Username'}
            return HttpResponse(render(request, 'index/register.html', output))
        if password != confirmPassword:
            output = {'error': 'Password does not match'}
            return HttpResponse(render(request, 'index/register.html', output))
        if len(name) == 0:
            output = {'error': 'Name cannot be blank'}
            return HttpResponse(render(request, 'index/register.html', output))
        hashedPassword = make_password(password)
        role_id = Role.objects.filter(name="Participant")[0].id
        user = User(username=username, password=hashedPassword, name=name, role_id=role_id)
        user.save()
        return redirect('/')

def administrator_index(request):
    return HttpResponse(render(request, 'index/administrator.html'))

def human_resources_department_index(request):
    ipp = 10
    page = getPage(request)
    allUsers = User.objects.all()
    if 'search' in request.GET:
        allUsers = allUsers.filter(username__icontains=request.GET['search'])
    allUsers = allUsers.filter(Q(role__name='Participant') | Q(role__name='Instructor'))
    users = allUsers[(page - 1) * ipp:page * ipp]
    totalPages = int(math.ceil(float(allUsers.count()) / float(ipp)))
    output = {'users': users, 'page': page, 'totalPages': totalPages}
    return HttpResponse(render(request, 'index/human-resources-department.html', output))

def instructor_index(request):
    output = {
        'categoriesLength': Category.objects.all().count(),
        'courses': Course.objects.filter(instructor=request.session['user_id']).order_by('-id'),
    }
    return HttpResponse(render(request, 'index/instructor.html', output))

def participant_index(request):
    output = {
        'categories': Category.objects.all().order_by('name')
    }
    output = getEnrolledCourse(request, output)
    return HttpResponse(render(request, 'index/participant.html', output))

def getEnrolledCourse(request, output):
    if not isParticipant(request):
        return output
    courses = EnrolledCourse.objects.filter(user=request.session['user_id']).filter(Q(status__name="In Progress") | Q(status__name="Retake") | Q(status__name="Completed"))
    for i, course in enumerate(courses):
        if course.status.name == "Completed":
            courses[i].progress = "%.2f" % 100
            courses[i].completed = True
        if course.status.name == "In Progress" or course.status.name == "Retake":
            modules = ModuleProgress.objects.filter(enrolled_course=course.id)
            completedModules = ModuleProgress.objects.filter(enrolled_course=course.id, status__name="Completed")
            if modules.count() != 0:
                componentPercentage = 0;
                if modules.count() != completedModules.count():
                    moduleProgress = ModuleProgress.objects.filter(enrolled_course=course.id, module__course=course.id, module__order_no=completedModules.count())[0]
                    componentProgressTotal = ComponentProgress.objects.filter(module_progress=moduleProgress.id).count()
                    componentProgressCompleted = ComponentProgress.objects.filter(module_progress=moduleProgress.id, status__name="Completed").count()
                    if componentProgressTotal != 0:
                        componentPercentage = (float(componentProgressCompleted) / float(componentProgressTotal)) * (float(1) / float(modules.count()))
                    else:
                        componentPercentage = float(1) / float(modules.count())
                courses[i].progress = "%.2f" % ((float(completedModules.count()) / float(modules.count()) + componentPercentage) * 100)
            else:
                courses[i].progress = "%.2f" % 100
    output['enrolled_courses'] = courses
    return output

def isAdministrator(request):
    return checkPermission(request, "Administrator")

def isHumanResourcesDepartment(request):
    return checkPermission(request, "Human Resources Department")

def isInstructor(request):
    return checkPermission(request, "Instructor")

def isParticipant(request):
    return checkPermission(request, "Participant")

def checkPermission(request, role):
    id = request.session['role_id']
    return Role.objects.filter(id=id, name=role).count() > 0

def invalidAccess():
    return HttpResponse('Invalid Access')

def getPage(request):
    if 'page' in request.GET:
        return int(request.GET['page'])
    return 1

class user:
    @staticmethod
    def list(request):
        if not isAdministrator(request):
            return invalidAccess()
        ipp = 10
        page = getPage(request)
        allUsers = User.objects.all()
        if 'search' in request.GET:
            allUsers = allUsers.filter(username__icontains=request.GET['search'])
        users = allUsers[(page - 1) * ipp:page * ipp]
        totalPages = int(math.ceil(float(allUsers.count()) / float(ipp)))
        output = {'users': users, 'page': page, 'totalPages': totalPages}
        return HttpResponse(render(request, 'user/list.html', output))

    @staticmethod
    def swap_instructor_role(request, user_id):
        if not isAdministrator(request):
            return invalidAccess()
        users = User.objects.filter(id=user_id)
        if users.count() == 1:
            user = users[0]
            if user.role.name == "Participant":
                parcipitantId = Role.objects.filter(name="Instructor")[0].id
                users.update(role=parcipitantId)
            elif user.role.name == "Instructor":
                instructorId = Role.objects.filter(name="Participant")[0].id
                users.update(role=instructorId)
        return redirect('../list')

    @staticmethod
    def completed_courses(request, user_id):
        user = User.objects.filter(id=user_id)
        if not isHumanResourcesDepartment(request) or user.count() == 0:
            return invalidAccess()
        user = user[0]
        courses = EnrolledCourse.objects.filter(user=user_id, status__name='Completed').order_by('-completion_date')
        output = {'user': user, 'courses': courses}
        return HttpResponse(render(request, 'user/completed_courses.html', output))
