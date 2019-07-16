# -*- coding: utf-8 -*-
from django.urls import path

from .views import (
	QueryOpenStreetMapSearch, QueryOpenStreetMapReverse
	)

app_name = 'openstreetmap'

urlpatterns = [
    path('search/', QueryOpenStreetMapSearch.as_view(), name="osm-search"),
    path('reverse/', QueryOpenStreetMapReverse.as_view(), name="osm-reverse"),
]
