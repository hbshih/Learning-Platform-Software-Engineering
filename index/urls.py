from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/list/$', views.user.list, name='user_list'),
    url(r'^user/swap_instructor_role/(?P<user_id>\d+)$', views.user.swap_instructor_role, name="swap_instructor_role"),
    url(r'^user/completed_courses/(?P<user_id>\d+)$', views.user.completed_courses, name='completed_courses')
]
