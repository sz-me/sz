from django.conf.urls.defaults import patterns, url
from sz.api import views

urlpatterns = patterns('',
    url(r'^$', 'sz.light.views.index', name='light-index'),
    url(r'^backbone/$', 'sz.light.views.backbone', name='light-backbone'),
)

