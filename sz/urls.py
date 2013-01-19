from django.conf.urls import patterns, include, url
from django.contrib import admin
from sz.core.forms import RegistrationForm

admin.autodiscover()





urlpatterns = patterns('',
    url(r'^$', 'sz.feed.views.index', name='feed-index'),
    url(r'^v/(?P<id>\w+)/$', 'sz.feed.views.place', name='feed-place'),
    url(r'^place_select/', 'sz.feed.views.place_select', name='feed-place_select'),
    url(r'^light/$', 'sz.feed.views.light', name='feed-light'),
    url(r'^api/', include('sz.api.urls'), name='api'),
    url(r'^accounts/register/$', 'registration.views.register',
        {
            'form_class': RegistrationForm,
            'backend': 'registration.backends.default.DefaultBackend'
        },
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
