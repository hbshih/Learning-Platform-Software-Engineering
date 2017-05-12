from django.http import HttpResponse

from course.models import Course
from course.module.models import Module
from course.module.component.models import Component, File

def index(request, file_id):
    file = File.objects.filter(id=file_id)
    if file.count() == 0:
        return HttpResponse('File Not Found')
    file = file[0]
    if not file.contents:
        return HttpResponse('File Not Found')
    response = HttpResponse(file.contents)
    response['Content-Type'] = 'application/force-download'
    response['Content-Disposition'] = 'attachment; filename="%s"' % file.name()
    return response
