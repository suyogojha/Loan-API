from django.conf.urls import url
from . import views
from .views import clientList

app_name='accounts'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^borrower/$',clientList.as_view(), name="clientlist" ),
	url(r'^borrower/update/(?P<id>\d+)/$',views.clientUpdate, name='update_client'),
	url(r'^borrower/create/$',views.createCLient, name='create_client'),
	url(r'^borrower/delete/(?P<id>\d+)/$', views.clientDelete, name='delete_client'),
	]

