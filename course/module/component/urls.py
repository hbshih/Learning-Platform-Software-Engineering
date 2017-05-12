from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<component_id>\d+)$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
]
