from django.conf.urls import url
from . import views 
from .views import HomeView


app_name='dashboard'
urlpatterns = [
   #/dashboard/
    url(r'^$',HomeView.as_view(),name='home'),
    url(r'^loan_type/$', views.loantype, name='loanType'),
    url(r'^product/create/$', views.product_create,name='create_product'),
    url(r'^product/update/(?P<id>\d+)/$', views.product_update, name="update_product"),
    url(r'^product/delete/(?P<id>\d+)/$', views.product_delete, name="delete_product"),
	]