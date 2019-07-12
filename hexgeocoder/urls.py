from django.urls import path, include


urlpatterns = [
    path('', include("openstreetmap.urls", namespace="osm")),
]
