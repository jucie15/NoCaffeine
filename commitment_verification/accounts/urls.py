from django.conf.urls import url, include
from django.contrib import admin
from accounts import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
]
