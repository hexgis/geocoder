# -*- coding: utf-8 -*-
import requests
import sys

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status

from .utils import request_search_data, request_reverse_data


class QueryOpenStreetMapSearch(APIView):
    """
    View utilizada para busca de locais a partir do endereço
    
    Args:
        location (str): location de busca na API nominatim
        scg (int): Ordem de coordenadas geograficas para a aplicação
            1 -> lon, lat
            2 -> lat, lon
        
    Returns:
        reponse (object): response com código de status e
            resposta da aplicação.
    """

    def post(self, request, **kwargs):
        q = self.request.data.get('location')
        if q is None:
            response = {"location": "Parameter is missing"}
            return Response(response, status=404)

        query = request_search_data(query=q)
        return Response(query['data'], status=query['status_code'])

    def get(self, request, format=None):
        q = request.GET.get('location', None)
        scg = request.GET.get('scg', None) or 1

        if q is None:
            response = {"location": "Parameter is missing"}
            return Response(response, status=404)

        query = request_search_data(query=q, scg=scg)
        return Response(query['data'], status=query['status_code'])


class QueryOpenStreetMapReverse(APIView):

    """
    View utilizada para geocodificação reversa utilizando nominatim

    Args:
        lat (float): ponto de latitude
        lon (float): ponto de longitude
        scg (int): Ordem de coordenadas geograficas para a aplicação
            1 -> lon, lat
            2 -> lat, lon

    Returns:
        reponse (object): response com código de status e
            resposta da aplicação.
    """

    def post(self, request, **kwargs):
        lat = self.request.data.get('lat')
        lon = self.request.data.get('lon')

        if lat is None:
            response = {"lat": "Parameter is missing"}
            return Response(response, status=404)
        if lon is None:
            response = {"lon": "Parameter is missing"}
            return Response(response, status=404)

        query = request_reverse_data(lat=lat, lon=lon)
        return Response(query['data'], status=query['status_code'])

    def get(self, request, format=None):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        if lat is None:
            response = {"lat": "Parameter is missing"}
            return Response(response, status=404)
        if lon is None:
            response = {"lon": "Parameter is missing"}
            return Response(response, status=404)

        scg = request.GET.get('scg', None) or 1
        query = request_reverse_data(lat=lat, lon=lon, scg=scg)
        return Response(query['data'], status=query['status_code'])