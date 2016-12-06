import requests
import pdb

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status

from geojson import Feature, Point, FeatureCollection

NOMINATIM_URL = "http://nominatim.openstreetmap.org/search"

def transform_request(json, scg):
    features = []
    for feat in json:
        lat = float(feat['lat'])
        lon = float(feat['lon'])
        properties = {"name": feat['display_name']}

        if scg == 1:
            point = Point((lon, lat))
        else:
            point = Point((lat, lon))

        features.append(
            Feature(
                geometry=Point((lon, lat)),
                properties=properties
            )
        )

    return {"data": FeatureCollection(features), "status_code": 200 }


def request_data(query, scg=1, url=NOMINATIM_URL):
    params = {"format": "json"}
    params["q"] = query

    try:
        r = requests.get(url, params=params)
    except Exception as Exc:
        return {"data":'API indisponível no momento', "status_code": 404}

    if r.status_code == 200:
        return transform_request(r.json(), scg)
    else:
        return {
            "data":'API indisponível no momento',
            "status_code": 404
        }

class QueryOpenStreetMap(APIView):

    def post(self, request, **kwargs):
        query = request_data(self.request.data)
        return Response(query['data'], status=query['status_code'])

    def get(self, request, format=None):
        endereco = request.GET.get('endereco', None)
        scg = request.GET.get('scg', None) or 1
        query = request_data(query=endereco, scg=scg)
        return Response(query['data'], status=query['status_code'])
