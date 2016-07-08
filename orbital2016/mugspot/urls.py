from django.conf.urls import url

from . import views

app_name = 'mugspot'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<place_id>[0-9]+)/$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^loggedin/$', views.logged_in_index, name='loggedinindex'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^updatelocation/$', views.update_location_view, name='update_location_view'),
]