from django.conf.urls import url
from . import views

app_name = 'hostel'

urlpatterns = [
    url(r'^$', views.about, name='about'),
    
    url(r'^index/$', views.index, name='index'),
    
    url(r'^login_user/$', views.login_user, name='login_user'),
    
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    
    url(r'^(?P<profile_id>[0-9]+)/$', views.detail, name='detail'),
    
    url(r'^files/(?P<filter_by>[a-zA_Z]+)/$', views.files, name='files'),
    
    url(r'^create_profile/$', views.create_profile, name='create_profile'),
    

    url(r'^(?P<profile_id>[0-9]+)/create_file/$', views.create_file, name='create_file'),
    
    url(r'^(?P<profile_id>[0-9]+)/delete_file/(?P<file_id>[0-9]+)/$', views.delete_file, name='delete_file'),
    
    url(r'^vote/(?P<profile_id>[0-9]+)/$', views.vote, name='vote'),

    url(r'^studentlist/$', views.studentlist, name='studentlist'),
    url(r'^information/$',views.messageinfo,name='messageinfo'),

]


