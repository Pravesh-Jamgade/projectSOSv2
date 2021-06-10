from django.contrib import admin
from django.conf.urls import url, include, re_path
from django.urls import path
from help_api.api.views import *

app_name = 'api'
urlpatterns = [
    
    path(r'register_entity/', RegisterEntityView.as_view(), name="save-entity-api"),
    path('entity/<str:name>/', getEntityDetail, name="get-named-entity-api"),
    path('entity/all/', getAllEntityDetails, name="get-all-entity-api"),
    path('sosgetall/', SOSView.as_view(), name="get-all-sos-view"),
    path('sospost/', SOSView.as_view(), name="save-sos-view"),
    path('sosgetone/(?P<pk>[a-zA-Z0-9-]+)/', SOSViewUpdate.as_view(), name="get-with-id-sos-view"),
    path('sosupdate/(?P<pk>[a-zA-Z0-9-]+)/', SOSViewUpdate.as_view(), name="update-sos-view"),
    

    # path('addr/<str:name>', AddressView.as_view(), name="get-addr-entity").
    path('addr/save', AddressView.as_view(), name="save-addr-entity"),

    #''' http://127.0.0.1:8000/help/toolsgetall?rate=6 '''
    path('toolsgetall/', ToolsView.as_view(), name="get-all-tools"),
    path('toolspost/', ToolsView.as_view(), name="save-tool"),
    
    
    #w
    url('test', test, name="test-api"),

]