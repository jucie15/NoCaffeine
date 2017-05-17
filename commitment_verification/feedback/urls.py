from django.conf.urls import url
from feedback import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^new/$', views.post_new, name='post_new'),
    url(r'^edit/(?P<post_pk>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^delete/(?P<post_pk>\d+)/$', views.post_delete, name='post_delete'),
    url(r'^(?P<post_pk>\d+)/comments/new/$', views.comment_new, name='comment_new'),
    url(r'^(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    url(r'^(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]


