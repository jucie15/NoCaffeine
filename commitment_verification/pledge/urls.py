from django.conf.urls import url
from pledge import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^congressman/$', views.congressman_list, name='congressman_list'),
    url(r'^congressman/party/(?P<party>\d{1})?/$', views.congressman_party, name='congressman_party'),
    url(r'^congressman/(?P<cm_pk>\d+)/$', views.congressman_detail, name='congressman_detail'),
    url(r'^pledge/$', views.pledge_list, name='pledge_list'),
    url(r'^pledge/(?P<pledge_pk>\d+)/$', views.pledge_detail, name='pledge_detail'),
    url(r'^pledge/(?P<pledge_pk>\d+)/comments/new/$', views.pledge_comment_new, name='pledge_comment_new'),
    url(r'^pledge/(?P<pledge_pk>\d+)/comments/(?P<comment_pk>\d+)/edit/$', views.pledge_comment_edit, name='pledge_comment_edit'),
    url(r'^pledge/(?P<pledge_pk>\d+)/comments/(?P<comment_pk>\d+)/delete/$', views.pledge_comment_delete, name='pledge_comment_delete'),
    url(r'^(?P<pledge_pk>\d+)/pledge_like/$', views
        .pledge_like, name='pledge_like'),
    url(r'^(?P<pledge_pk>\d+)/pledge_dislike/$', views.pledge_dislike, name='pledge_dislike'),
    url(r'^search/$', views.search, name='search'),
]
