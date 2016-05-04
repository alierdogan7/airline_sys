from django.conf.urls import url
from . import views

urlpatterns = [ 
	url(r'^$', views.index, name='index'),
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
	url(r'^crew/$', views.crew_index, name='crew_index'),

	# yusuf
	url(r'^cust_log/$', views.cust_log, name='cust_log'),
	url(r'^cust(?P<cust_id>[0-9]+)/index/$', views.cust_index, name='cust_index'),
]