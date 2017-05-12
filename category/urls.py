from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<category_id>\d+)$', views.index, name='index'),
    url(r'^list$', views.list, name='list'),
    url(r'^add$', views.add, name='add'),
    url(r'^delete/(?P<category_id>\d+)$', views.delete, name="delete"),
    url(r'^edit/(?P<category_id>\d+)$', views.edit, name="edit"),
]
