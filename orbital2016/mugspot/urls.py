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
]
