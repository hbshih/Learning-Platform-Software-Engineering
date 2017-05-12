from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect

from index.views import isInstructor, isParticipant, invalidAccess, getEnrolledCourse

from ...models import Status, Course, EnrolledCourse
from ..models import Module, ModuleProgress
from .models import ComponentType, Component, ComponentProgress, Text, Image, File, Quiz, Youtube

from .forms import ImageForm, FileForm

import json

# Create your views here.
def index(request, course_id, module_id, component_id):
    if isParticipant(request):
        course_id = int(course_id)
        component = Component.objects.filter(id=component_id, module=module_id)
        if component.count() == 0:
            return invalidAccess()
        component = component[0]
        if component.module.course.id != course_id:
            return invalidAccess()
        inProgress = Status.objects.filter(name="In Progress")[0]
        completed = Status.objects.filter(name="Completed")[0]
        dropped = Status.objects.filter(name="Dropped")[0].id
        enrolledCourse = EnrolledCourse.objects.filter(course=course_id, user=request.session['user_id'])
        if enrolledCourse.count() == 0:
            return redirect('/course/' + str(course_id) + '/overview')
        enrolledCourse = enrolledCourse[0]
        currentStatus = enrolledCourse.status.id
        if currentStatus == dropped:
            return redirect('/course/' + str(course_id) + '/overview')
        moduleProgress = ModuleProgress.objects.filter(enrolled_course=enrolledCourse.id, module=module_id)
        if moduleProgress.count() == 0:
            module = Module.objects.filter(id=module_id, course=course_id)
            moduleProgress = ModuleProgress(enrolled_course=enrolledCourse, module=module, status=inProgress)
            moduleProgress.save()
        else:
            moduleProgress = moduleProgress[0]
        componentProgress = ComponentProgress.objects.filter(module_progress=moduleProgress, component=component_id)
        if componentProgress.count() == 0:
            component = Component.objects.filter(id=component_id, module=module_id)
            componentProgress = ComponentProgress(module_progress=moduleProgress, component=component, status=completed)
        else:
            componentProgress.update(status=completed)
        componentProgressTotal = ComponentProgress.objects.filter(module_progress=moduleProgress).count()
        componentProgressCompleted = ComponentProgress.objects.filter(module_progress=moduleProgress, status=completed.id).count()
        if componentProgressCompleted == componentProgressTotal:
            moduleProgress = ModuleProgress.objects.filter(enrolled_course=enrolledCourse.id, module=module_id)
            moduleProgress.update(status=completed)
        output = {'component': component}
        output = getEnrolledCourse(request, output)
        def view_specific_component(request, output):
            switcher = {
                "Text": viewText,
                "Image": viewImage,
                "File": viewFile,
                "Quiz": viewQuiz,
                "Youtube": viewYoutube,
            }
            type = output['component'].type.name
            reference = output['component'].reference
            return switcher.get(type)(request, output, reference)
        return view_specific_component(request, output)
    if isInstructor(request):
        course = Course.objects.filter(id=course_id)
        module = Module.objects.filter(id=module_id, course=course_id)
        component = Component.objects.filter(id=component_id, module=module_id)
        if course.count() == 0 or module.count() == 0 or component.count() == 0:
            return invalidAccess()
        course = course[0]
        module = module[0]
        component = component[0]
        if course.instructor.id != request.session['user_id']:
            return InvalidAccess()
        output = {'course': course, 'module': module, 'component': component}
        if request.method == 'POST':
            def save_specific_component(request, output):
                switcher = {
                    "Text": saveText,
                    "Image": saveImage,
                    "File": saveFile,
                    "Quiz": saveQuiz,
                    "Youtube": saveYoutube,
                }
                type = output['component'].type.name
                reference = output['component'].reference
                return switcher.get(type)(request, output, reference)
            return save_specific_component(request, output)
        def render_specific_component(request, output):
            switcher = {
                "Text": renderText,
                "Image": renderImage,
                "File": renderFile,
                "Quiz": renderQuiz,
                "Youtube": renderYoutube,
            }
            type = output['component'].type.name
            reference = output['component'].reference
            return switcher.get(type)(request, output, reference)
        return render_specific_component(request, output)
    return invalidAccess()

def add(request, course_id, module_id):
    if not isInstructor(request):
        return invalidAccess()
    course = Course.objects.filter(id=course_id)
    module = Module.objects.filter(id=module_id, course=course_id)
    if course.count() == 0 or module.count() == 0:
        return invalidAccess()
    course = course[0]
    module = module[0]
    if 'name' not in request.POST or 'type' not in request.POST:
        types = ComponentType.objects.all().order_by('id')
        output = {'course': course, 'module': module, 'types': types}
        return HttpResponse(render(request, 'course/module/component/add.html', output))
    if course.instructor.id != request.session['user_id']:
        return invalidAccess()
    name = request.POST['name']
    type = ComponentType.objects.filter(id=request.POST['type'])
    if type.count() == 0:
        return invalidAccess()
    type = type[0]
    def create_specific_component(type):
        switcher = {
            "Text": createNewText,
            "Image": createNewImage,
            "File": createNewFile,
            "Quiz": createNewQuiz,
            "Youtube": createNewYoutube,
        }
        return switcher.get(type.name)()
    reference = create_specific_component(type)
    lastComponent = Component.objects.filter(module=module_id).order_by('order_no')
    order_no = lastComponent.count()
    component = Component(name=name, module=module, type=type, order_no=order_no, reference=reference)
    component.save()
    return redirect('/course/' + str(course_id) + '/module/' + str(module_id) + '/component/' + str(component.id))

def createNewText():
    text = Text(contents='')
    text.save()
    return text.id

def saveText(request, output, reference):
    course_id = output['course'].id
    module_id = output['module'].id
    text = Text.objects.filter(id=reference)
    if 'contents' not in request.POST or text.count() == 0:
        return invalidAccess()
    contents = request.POST['contents']
    text.update(contents=contents)
    return redirect('/course/' + str(course_id) + '/module/' + str(module_id))

def renderText(request, output, reference):
    text = Text.objects.filter(id=reference)
    if text.count() == 0:
        return invalidAccess()
    output['text'] = text[0]
    return HttpResponse(render(request, 'course/module/component/text.html', output))

def viewText(request ,output, reference):
    text = Text.objects.filter(id=reference)
    if text.count() == 0:
        return invalidAccess()
    output['text'] = text[0]
    return HttpResponse(render(request, 'course/module/component/view-text.html', output))

def createNewImage():
    image = Image(contents='')
    image.save()
    return image.id

def saveImage(request, output, reference):
    course_id = output['course'].id
    module_id = output['module'].id
    image = Image.objects.filter(id=reference)
    image_form = ImageForm(request.POST, request.FILES)
    if image.count() == 0 or not image_form.is_valid():
        return HttpResponse('No image selected.')
    image = image[0]
    image.contents= image_form.cleaned_data['image']
    image.save()
    return redirect('/course/' + str(course_id) + '/module/' + str(module_id))

def renderImage(request, output, reference):
    image = Image.objects.filter(id=reference)
    if image.count() == 0:
        return invalidAccess()
    output['image'] = image[0]
    return HttpResponse(render(request, 'course/module/component/image.html', output))

def viewImage(request ,output, reference):
    image = Image.objects.filter(id=reference)
    if image.count() == 0:
        return invalidAccess()
    output['image'] = image[0]
    return HttpResponse(render(request, 'course/module/component/view-image.html', output))

def createNewFile():
    file = File(contents='')
    file.save()
    return file.id

def saveFile(request, output, reference):
    course_id = output['course'].id
    module_id = output['module'].id
    file = File.objects.filter(id=reference)
    file_form = FileForm(request.POST, request.FILES)
    if file.count() == 0 or not file_form.is_valid():
        return HttpResponse('No file selected.')
    file = file[0]
    file.contents = file_form.cleaned_data['file']
    file.save()
    return redirect('/course/' + str(course_id) + '/module/' + str(module_id))

def renderFile(request, output, reference):
    file = File.objects.filter(id=reference)
    if file.count() == 0:
        return invalidAccess()
    output['file'] = file[0]
    return HttpResponse(render(request, 'course/module/component/file.html', output))

def viewFile(request, output, reference):
    file = File.objects.filter(id=reference)
    if file.count() == 0:
        return invalidAccess()
    return redirect('/download/' + str(file[0].id))

def createNewQuiz():
    quiz_type = ComponentType.objects.filter(name="Quiz")[0]
    lastQuizId = Component.objects.filter(type=quiz_type.id).order_by('-reference')
    if lastQuizId.count() > 0:
        quiz_id = lastQuizId[0].reference
        return quiz_id + 1
    return 1

def saveQuiz(request, output, reference):
    course_id = output['course'].id
    module_id = output['module'].id
    if 'questions' not in request.POST or 'answers' not in request.POST:
        return invalidAccess()
    questions = json.loads(request.POST['questions'])
    answers = json.loads(request.POST['answers'])
    if len(questions) != len(answers):
        return invalidAccess()
    originalQuizes = Quiz.objects.filter(quiz_id=reference).order_by('-question_no')
    for i in range(originalQuizes.count() - 1, len(questions) - 1, -1):
        Quiz.objects.get(pk=originalQuizes[i].id).delete()
    for i in range(0, len(questions)):
        if i < originalQuizes.count():
            quiz = Quiz.objects.filter(id=originalQuizes[len(questions) - i - 1].id)
            quiz.update(question=questions[i], answer=answers[i])
        else:
            quiz = Quiz(quiz_id=reference, question_no=i, question=questions[i], answer=answers[i])
            quiz.save()
    return HttpResponse('/course/' + str(course_id) + '/module/' + str(module_id))
   

def renderQuiz(request, output, reference):
    quizes = Quiz.objects.filter(quiz_id=reference)
    output['quizes'] = quizes
    return HttpResponse(render(request, 'course/module/component/quiz.html', output))

def viewQuiz(request, output, reference):
    quizes = Quiz.objects.filter(quiz_id=reference).order_by('question_no')
    if request.method == 'POST' and 'answers' in request.POST:
        answers = json.loads(request.POST['answers'])
        data = []
        for i, quiz in enumerate(quizes):
            if quiz.answer.lower() == answers[i].lower():
                correct = True
            else:
                correct = False
            data.append({'answer': quiz.answer, 'correct': correct})
        data = json.dumps(data)
        return HttpResponse(data)
    output['quizes'] = quizes
    return HttpResponse(render(request, 'course/module/component/view-quiz.html', output))

def createNewYoutube():
    youtube = Youtube(video='')
    youtube.save()
    return youtube.id

def saveYoutube(request, output, reference):
    course_id = output['course'].id
    module_id = output['module'].id
    youtube = Youtube.objects.filter(id=reference)
    if 'video' not in request.POST or youtube.count() == 0:
        return invalidAccess()
    video = request.POST['video']
    youtube.update(video=video)
    return redirect('/course/' + str(course_id) + '/module/' + str(module_id))

def renderYoutube(request, output, reference):
    youtube = Youtube.objects.filter(id=reference)
    if youtube.count() == 0:
        return invalidAccess()
    output['youtube'] = youtube[0]
    return HttpResponse(render(request, 'course/module/component/youtube.html', output))

def viewYoutube(request ,output, reference):
    youtube = Youtube.objects.filter(id=reference)
    if youtube.count() == 0:
        return invalidAccess()
    output['youtube'] = youtube[0]
    return HttpResponse(render(request, 'course/module/component/view-youtube.html', output))
