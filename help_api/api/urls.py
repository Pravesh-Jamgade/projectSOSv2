from django.contrib import admin
from django.conf.urls import url, include
from help_api.api.views import *

app_name = 'api'
urlpatterns = [
    url('get/address/', AddressView.as_view(), name="address-all-entity-api"),
    url('get/address/(?P<id>[0-9a-z]{32}\Z)/$',
        AddressView.as_view(), name="address-entity-api"),

    url('save/entity/', RegisterEntityView.as_view(), name="save-entity-api"),
    url('get/entity/', EntityView.as_view(), name="get-all-entity-api"),
    url('get/entity/<entity_name>/', EntityView.as_view(),
        name="get-named-entity-api"),

    url('get/sosinfo/', SOSView.as_view(),
        name="get-sosinfo-api"),

]
