from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.GilKvarList.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', views.GilKvarList.as_view(), name='list_upl'),
    url(r'^new/$', views.GilKvarCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/update/$', views.GilKvarUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.GilKvarDelete.as_view(), name='delete'),

    url(r'^flats/(?P<fk>\d+)/$', views.FlatList.as_view(), name='flats'),
    url(r'^flat/new/(?P<fk>\d+)/$', views.FlatCreate.as_view(), name='create_flat'),
    url(r'^flat/(?P<pk>\d+)/update/$', views.FlatUpdate.as_view(), name='update_flat'),
    url(r'^flat/(?P<pk>\d+)/delete/$', views.FlatDelete.as_view(), name='delete_flat'),

    url(r'^(?P<pk>\d+)/uploadflats/$', views.uploadflats, name='uploadflats'),
    url(r'^(?P<pk>\d+)/getdata/(?P<outputformat>[\w-]+)$', views.getdata, name='getdata'),

    url(r'^accounts/login/', views.signin, name='signin'),
    url(r'^logout/', views.dologout, name='logout'),

]
