from django.conf.urls import include, url

from .component import urls

from . import views

urlpatterns = [
    url(r'^(?P<module_id>\d+)$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^(?P<module_id>\d+)/save_order$', views.save_order, name="save_order"),
    url(r'^(?P<module_id>\d+)/component/', include(urls)),
]
