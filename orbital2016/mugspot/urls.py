from django.conf.urls import url

from . import views

app_name = 'mugspot'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<place_id>[0-9]+)/$', views.index, name='index'),
	url(r'^usrprof/(?P<user_id>[0-9]+)/$', views.user_profile_view, name='user_profile_view'),
        url(r'^about/$', views.about, name='about'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^allpos/$', views.all_positions_view, name='position'),
	url(r'^checklginjs/$', views.check_login_js_view, name='checklginjs'),
	url(r'^usrprof/$', views.user_profile_view, name='user_profile_view'),
	url(r'^updfriends/$', views.update_friends_view, name='tellfriendsview'),
	url(r'^arv/$', views.accept_request_view, name='accept_request_view'),
	url(r'^drv/$', views.delete_request_view, name='delete_request_view'),
	url(r'^crv/$', views.create_request_view, name='create_request_view'),
	url(r'^urv/$', views.undo_request_view, name='undo_request_view'),
	url(r'^updacc/$', views.update_account_view, name='update_account_view'),
]
