# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib import admin

from .views import (
    QueryOpenStreetMapSearch, QueryOpenStreetMapReverse, index
)

app_name = 'openstreetmap'

urlpatterns = [
    path('search/', QueryOpenStreetMapSearch.as_view(), name="osm-search"),
    path('reverse/', QueryOpenStreetMapReverse.as_view(), name="osm-reverse"),
    path('', index, name="index"),
]
