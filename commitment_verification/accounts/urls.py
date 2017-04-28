from django.conf.urls import url, include
from django.contrib import admin
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={'next_page': 'pledge:index'}),
]
