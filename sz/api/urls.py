from django.conf.urls.defaults import patterns, url
from sz.api import views as root
from sz.api.views import auth, categories, cities, messages, places, users


urlpatterns = patterns('',
    url(r'^$', root.ApiRoot.as_view()),
    url(r'^categories$', categories.CategoriesRoot.as_view(), name='category-list'),
    url(r'^categories/detect$', categories.CategoriesDetect.as_view(), name='category-detect'),
    url(r'^categories/(?P<pk>\w+)$', categories.CategoriesInstance.as_view(), name='category-detail'),
    url(r'^messages/(?P<pk>\d+)$', messages.MessageInstance.as_view(), name='message-detail'),
    url(r'^messages/(?P<pk>\d+)/photo$', messages.MessageInstancePhoto.as_view(), name='message-detail-photo'),
    url(r'^messages/previews/(?P<pk>\d+)/publish', messages.MessagePreviewInstancePublish.as_view(),
        name='message-preview-publish'),
    url(r'^messages/previews/(?P<pk>\d+)', messages.MessagePreviewInstance.as_view(), name='message-previews-detail'),
    url(r'^users/self$', users.UserInstanceSelf.as_view(), name='user-detail-self'),
    url(r'^places/newsfeed$', places.PlaceRootNewsFeed.as_view(), name='place-newsfeed'),
    url(r'^places/search$', places.PlaceSearch.as_view(), name='place-search'),
    url(r'^places/venues/search$', places.PlaceVenueSearch.as_view(), name='place-venue-search'),
    url(r'^places/(?P<pk>\w+)/newsfeed$', places.PlaceInstanceNewsFeed.as_view(), name='place-detail-newsfeed'),
    url(r'^places/(?P<pk>\w+)/messages$', places.PlaceInstanceMessages.as_view(), name='place-detail-messages'),
    url(r'^places/(?P<pk>\w+)/messages/previews$', places.PlaceInstanceMessagePreviews.as_view(),
        name='place-detail-message-preview'),
    url(r'^places/(?P<pk>\w+)$', places.PlaceInstance.as_view(), name='place-detail'),
    url(r'^cities/nearest$', cities.CityNearest.as_view(), name='city-nearest'),
    url(r'^auth/login$', auth.AuthLogin.as_view(), name='auth-login'),
    url(r'^auth/logout$', auth.AuthLogout.as_view(), name='auth-logout'),
    url(r'^auth/user$', auth.AuthUser.as_view(), name='auth-user'),
    #url(r'^authentication$', views.Authentication.as_view(), name='token-auth-authenticate'),
)

