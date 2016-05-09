from django.conf.urls import url
from . import views

urlpatterns = [ 
	url(r'^$', views.index, name='index'),
	url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
	url(r'^admin/reports$', views.reports, name='reports'),
	# yusuf
	url(r'^cust_log/$', views.cust_log, name='cust_log'),
	url(r'^cust_log/(?P<fl_id>[0-9]+)$', views.fl_view, name='fl_view'),
	url(r'^cust_index/$', views.cust_index, name='cust_index'),
	url(r'^cust_log/ticket$', views.cust_tickets, name='cust_tickets'),
	url(r'^cust_log/profile$', views.cust_profile, name='cust_profile'),
	url(r'^cust_log/new_reserv$', views.new_reserv, name='new_reserv'),
	url(r'^cust_logout/$', views.cust_logout, name='cust_logout'),
	url(r'^crew_log/$', views.crew_log, name='crew_log'),
	url(r'^create_account/$', views.create_account, name='create_account'),
	url(r'^cust(?P<cust_id>[0-9]+)/index/$', views.cust_index, name='cust_index'),
]