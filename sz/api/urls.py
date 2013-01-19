from django.conf.urls.defaults import patterns, url
from sz.api import views

urlpatterns = patterns('',
    url(r'^$', views.ApiRoot.as_view()),
    url(r'^messages/(?P<pk>\d+)/$', views.MessageInstance.as_view(), name='message-detail'),
    url(r'^users/$', views.UserRoot.as_view(), name='user-list'),
    url(r'^places/$', views.PlaceRoot.as_view(), name='place-list'),
    url(r'^places/(?P<pk>\w+)/$', views.PlaceInstance.as_view(), name='place-detail'),
    url(r'^places/(?P<pk>\w+)/messages/$', views.PlaceMessages.as_view(), name='place-messages'),
    url(r'^cities/$', views.CityRoot.as_view(), name='city-list'),
    url(r'^authentication/$', views.Authentication.as_view(), name='token-auth-authenticate'),
)

