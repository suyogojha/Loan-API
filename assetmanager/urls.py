from django.conf.urls import url
from . import views 


app_name='assetmanager'
urlpatterns = [
    url(r'^$', views.assetList.as_view(), name='assetlist'),
    url(r'^create/$', views.createAsset, name='create_asset'),
    url(r'^update/(?P<id>\d+)/$', views.asset_update, name="update_asset"),
    url(r'^delete/(?P<id>\d+)/$', views.asset_delete, name="delete_asset"),
	]