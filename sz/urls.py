from django.conf.urls import patterns, include, url
from sz.api.views import PlaceSearchView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sz.feed.views.home', name='home'),
    url(r'^$', 'sz.feed.views.index'),
    url(r'^api/tags$', 'sz.api.views.tags'),
    url(r'^api/places/search$', PlaceSearchView.as_view(), name='places-root'),
    # url(r'^sz/', include('sz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^restframework', include('djangorestframework.urls', namespace='djangorestframework')),
)
