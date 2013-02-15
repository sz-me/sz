from django.conf.urls.defaults import patterns, url
from sz.api import views

urlpatterns = patterns('',
    url(r'^$', views.ApiRoot.as_view()),
    url(r'^categories$', views.CategoriesRoot.as_view(), name='category-list'),
    url(r'^categories/detect$', views.CategoriesDetect.as_view(), name='category-detect'),
    url(r'^categories/(?P<pk>\w+)$', views.CategoriesInstance.as_view(), name='category-detail'),
    url(r'^messages/(?P<pk>\d+)$', views.MessageInstance.as_view(), name='message-detail'),
    url(r'^users$', views.UserRoot.as_view(), name='user-list'),
    url(r'^places/feed$', views.PlaceFeed.as_view(), name='place-feed'),
    url(r'^places/search$', views.PlaceSearch.as_view(), name='place-search'),
    url(r'^places/(?P<pk>\w+)$', views.PlaceInstance.as_view(), name='place-detail'),
    url(r'^places/(?P<pk>\w+)/messages$', views.PlaceMessages.as_view(), name='place-messages'),
    url(r'^cities/nearest$', views.CityNearest.as_view(), name='city-nearest'),
    url(r'^authentication$', views.Authentication.as_view(), name='token-auth-authenticate'),
)

