from django.conf.urls.defaults import patterns, url
from sz.api import views

urlpatterns = patterns('',
    url(r'^$', views.ApiRoot.as_view()),
    url(r'^messages/$', views.MessageRoot.as_view(), name='message-list'),
    url(r'^messages/(?P<pk>\d+)/$', views.MessageInstance.as_view(), name='message-detail'),
    url(r'^users/$', views.UserRoot.as_view(), name='user-list'),
    url(r'^places/$', views.PlaceRoot.as_view(), name='place-list'),
    url(r'^cities/$', views.CityRoot.as_view(), name='city-list'),
    url(r'^things/$', views.ThingRoot.as_view(), name='thing-list'),
    url(r'^categories/$', views.CategoryRoot.as_view(), name='category-list'),
)

