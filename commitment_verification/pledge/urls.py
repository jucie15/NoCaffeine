from django.conf.urls import url
from django.contrib import admin
from pledge import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^congressman/$', views.congressman_list, name='congressman_list'),
    url(r'^congressman/(?P<pk>\d+)/$', views.congressman_detail, name='congressman_detail'),
    url(r'^pledge/$', views.pledge_list, name='pledge_list'),
    url(r'^search/$', views.search, name='search'),

]
