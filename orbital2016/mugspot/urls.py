from django.conf.urls import url

from . import views

app_name = 'mugspot'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<place_id>[0-9]+)/$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^allpos/$', views.all_positions_view, name='position'),
	url(r'^checklginjs/$', views.check_login_js_view, name='checklginjs'),
	url(r'^usrprof/$', views.user_profile_view, name='user_profile_view'),
	url(r'^usrprof/$', views.update_friends_view, name='tellfriendsview'),
	url(r'^usrprof/$', views.friend_request_view, name='friend_request_view'),
]
