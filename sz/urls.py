from django.conf.urls import patterns, include, url
from django.contrib import admin
from sz import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^client/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.CLIENT_ROOT,
        }),
    url(r'^/?$', 'sz.core.views.index', name='client-index'),
    url(r'^confirm/(?P<confirmation_key>.*)/?$', 'sz.core.views.confirm', 
        name='registration-confirm'),
    url(r'^api/', include('sz.api.urls'), name='api'),
    #url(r'^vj-detection-demo/', 'sz.vjdetection.views.index', name='vj-detection-demo'),
    #url(r'^accounts/register/$', 'registration.views.register',
    #    {
    #        'form_class': RegistrationForm,
    #        'backend': 'registration.backends.default.DefaultBackend'
    #    },
    #    name='registration_register'),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
