from django.conf.urls import include, url

from .module import urls

from . import views

urlpatterns = [
    url(r'^(?P<course_id>\d+)$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^(?P<course_id>\d+)/open$', views.open, name='open'),
    url(r'^(?P<course_id>\d+)/close$', views.close, name='close'),
    url(r'^(?P<course_id>\d+)/save_order', views.save_order, name='save_order'),
    url(r'^(?P<course_id>\d+)/overview', views.overview, name='overview'),
    url(r'^(?P<course_id>\d+)/enroll', views.enroll, name='enroll'),
    url(r'^(?P<course_id>\d+)/drop', views.drop, name='drop'),
    url(r'^(?P<course_id>\d+)/module/', include(urls)),
]
