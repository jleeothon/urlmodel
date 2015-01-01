from django.conf.urls import patterns
from django.conf.urls import url

from .views import test_view

urlpatterns = patterns(
    '',

    url(r'^regions/?$', test_view, name='region-list'),
    url(r'^regions/new/?$', test_view, name='region-create'),
    url(r'^regions/(?P<name>[\w-]+)/?$', test_view, name='region-create'),
    url(r'^regions/(?P<name>[\w-]+)/edit/?$', test_view, name='region-update'),
    url(r'^regions/(?P<name>[\w-]+)/delete/?$', test_view,
        name='region-delete'),

    url(r'^regions/(?P<region>[\w-]+)/(?P<name>)/?$', test_view,
        name='town-detail'),
    url(r'^regions/(?P<region>[\w-]+)/(?P<name>)/edit/?$', test_view,
        name='town-update'),
    url(r'^regions/(?P<region>[\w-]+)/(?P<name>)/delete/?$', test_view,
        name='town-update'),
       
)
