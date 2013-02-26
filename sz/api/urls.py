from django.conf.urls.defaults import patterns, url
from sz.api import views

urlpatterns = patterns('',
    url(r'^$', views.ApiRoot.as_view()),
    url(r'^categories$', views.CategoriesRoot.as_view(), name='category-list'),
    url(r'^categories/detect$', views.CategoriesDetect.as_view(), name='category-detect'),
    url(r'^categories/(?P<pk>\w+)$', views.CategoriesInstance.as_view(), name='category-detail'),
    url(r'^messages/(?P<pk>\d+)$', views.MessageInstance.as_view(), name='message-detail'),
    url(r'^users/self$', views.UserInstanceSelf.as_view(), name='user-detail-self'),
    url(r'^places/newsfeed$', views.PlaceRootNewsFeed.as_view(), name='place-newsfeed'),
    url(r'^places/search$', views.PlaceSearch.as_view(), name='place-list-search'),
    url(r'^places/(?P<pk>\w+)/newsfeed$', views.PlaceInstanceNewsFeed.as_view(), name='place-detail-newsfeed'),
    url(r'^places/(?P<pk>\w+)/messages$', views.PlaceInstanceMessages.as_view(), name='place-detail-messages'),
    url(r'^places/(?P<pk>\w+)$', views.PlaceInstance.as_view(), name='place-detail'),
    url(r'^cities/nearest$', views.CityNearest.as_view(), name='city-nearest'),
    url(r'^auth/login$', views.AuthLogin.as_view(), name='auth-login'),
    url(r'^auth/logout$', views.AuthLogout.as_view(), name='auth-logout'),
    url(r'^authentication$', views.Authentication.as_view(), name='token-auth-authenticate'),
)

