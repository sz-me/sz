from django.conf.urls import patterns, include, url
from sz.api import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/$', views.ApiRoot.as_view()),
    url(r'^api/messages/$', views.MessageRoot.as_view(), name='message-list'),
    url(r'^api/messages/(?P<pk>\d+)/$', views.MessageInstance.as_view(), name='message-detail'),
    url(r'^api/users/$', views.UserRoot.as_view(), name='user-list'),
    url(r'^api/places/$', views.PlaceRoot.as_view(), name='place-list'),
    #url(r'^api/tags$', 'sz.api.views.tags'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
