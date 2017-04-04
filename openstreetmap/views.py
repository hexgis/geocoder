# -*- coding: utf-8 -*-
import requests
import sys

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status

from geojson import Feature, Point, FeatureCollection

NOMINATIM_URL = "http://nominatim.openstreetmap.org/search"
NOMINATIM_URL_REVERSE = "http://nominatim.openstreetmap.org/reverse"
REQUEST_ERROR_DATA = {
        "data":'API indisponível no momento', 
        "status_code": 404
}


def error_response_exception(exc):
    return Response(
        {"data": exc},
        status=404
        )

def transform_request(json, scg=1, search_type="search"):
    """ Função para transofração da requisição em geojson
    json: dado de entrada
    scg: sistema de coordenadas (
        1 -> lon, lat
        2 -> lat, lon
        )
    """
    if search_type == "search":

        features = []
        for feat in json:
            lat = float(feat['lat'])
            lon = float(feat['lon'])
            properties = {"name": feat['display_name']}

            point = Point((lat, lon))

            if scg == 1:
                point = Point((lon, lat))

            features.append(
                Feature(
                    geometry=point,
                    properties=properties
                )
            )

        return {"data": FeatureCollection(features), "status_code": 200 }

    if search_type == "reverse":

        if 'error' in json:
            return {"data": FeatureCollection({
                'Erro de geocodificação, ponto sem informação'
                }) , "status_code": 200 }

        feature = []
        properties = {}
        lat = float(json['lat'])
        lon = float(json['lon'])

        properties["name"] = json['display_name']
        properties["address"] = json['address']

        point = Point((lat, lon))

        if scg == 1:
            point = Point((lon, lat))

        feature.append(
            Feature(
                geometry=point,
                properties=properties
            )
        )

        return {"data": FeatureCollection(feature), "status_code": 200 }

def request_search_data(query, scg=1, url=NOMINATIM_URL):
    """ Função para requisição dos dados no nominatim
    query: pesquisa realizada
    scg: sistema de coordenadas (
        1 -> lon, lat
        2 -> lat, lon
        )
    url: url de pesquisa do nominatim
    """
    params = {}
    params["q"] = query
    params["format"] = 'json'
    params["polygon"] = 1

    try:
        r = requests.get(url, params=params)
    except Exception as Exc:
        return REQUEST_ERROR_DATA

    if r.status_code == 200:
        return transform_request(r.json(), scg, search_type="search")

    return REQUEST_ERROR_DATA

def request_reverse_data(lat, lon, scg=1, url=NOMINATIM_URL_REVERSE):
    """ 
    Função para requisição dos dados no nominatim
    lat: ponto decimal para latitude
    lon: ponto decimal para longitude
    scg: sistema de coordenadas (
        1 -> lon, lat
        2 -> lat, lon
        )
    url: url de pesquisa do nominatim
    """
    params = {}
    params["lat"] = float(lat)
    params["lon"] = float(lon)
    params["format"] = 'json'

    try:
        r = requests.get(url, params=params)
    except Exception as Exc:
        return REQUEST_ERROR_DATA

    if r.status_code == 200:
        return transform_request(r.json(), scg, search_type="reverse")

    return REQUEST_ERROR_DATA


class QueryOpenStreetMapSearch(APIView):
    """
    View utilizada para busca de locais a partir do endereço

    endereco: endereco de busca na API nominatim
    scg: sistema de coordenadas geográficas
        1 -> lon, lat
        2 -> lat, lon
    """

    def post(self, request, **kwargs):
        end = self.request.data.get('endereco')

        if end is None:
            return error_response_exception('endereco is missing')

        query = request_search_data(query=endereco)
        return Response(query['data'], status=query['status_code'])

    def get(self, request, format=None):
        endereco = request.GET.get('endereco', None)
        scg = request.GET.get('scg', None) or 1

        if endereco is None:
            error_response_exception('endereco is missing')

        query = request_search_data(query=endereco, scg=scg)
        return Response(query['data'], status=query['status_code'])


class QueryOpenStreetMapReverse(APIView):

    """
    View utilizada para busca de locais a partir do endereço

    lat: latitude 
    lon: longitude
    scg: sistema de coordenadas geográficas
        1 -> lon, lat
        2 -> lat, lon
    """

    def post(self, request, **kwargs):
        lat = self.request.data.get('lat')
        lon = self.request.data.get('lon')

        if lat is None:
            return error_response_exception('latitude is missing')
        if lon is None:
            return error_response_exception('longitude is missing')

        query = request_reverse_data(lat=lat, lon=lon)
        return Response(query['data'], status=query['status_code'])

    def get(self, request, format=None):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        if lat is None:
            return error_response_exception('latitude is missing')
        if lon is None:
            return error_response_exception('longitude is missing')
    
        scg = request.GET.get('scg', None) or 1
        query = request_reverse_data(lat=lat, lon=lon, scg=scg)
        return Response(query['data'], status=query['status_code'])