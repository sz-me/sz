from django.conf.urls.defaults import patterns, url
from sz.api import views

urlpatterns = patterns('',
    url(r'^$', views.ApiRoot.as_view()),
    url(r'^messages/$', views.MessageRoot.as_view(), name='message-list'),
    url(r'^messages/(?P<pk>\d+)/$', views.MessageInstance.as_view(), name='message-detail'),
    url(r'^users/$', views.UserRoot.as_view(), name='user-list'),
    url(r'^places/$', views.PlaceRoot.as_view(), name='place-list'),
    url(r'^places/(?P<pk>\w+)/$', views.PlaceInstance.as_view(), name='place-detail'),
    url(r'^places/(?P<pk>\w+)/messages/$', views.PlaceMessages.as_view(), name='place-messages'),
    url(r'^cities/$', views.CityRoot.as_view(), name='city-list'),
    url(r'^things/$', views.ThingRoot.as_view(), name='thing-list'),
    url(r'^things/(?P<pk>\w+)/$', views.ThingInstance.as_view(), name='thing-detail'),
    url(r'^things/(?P<pk>\w+)/messages/$', views.ThingMessages.as_view(), name='thing-messages'),
    url(r'^categories/$', views.CategoryRoot.as_view(), name='category-list'),
    url(r'^categories/(?P<pk>\w+)/$', views.CategoryRoot.as_view(), name='category-detail'),
    url(r'^categories/(?P<pk>\w+)/messages/$', views.ThingRoot.as_view(), name='category-messages'),
)

