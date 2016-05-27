from django.conf.urls import url

from . import views

app_name = 'mugspot'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<place_id>[0-9]+)/$', views.index, name='index'),
]