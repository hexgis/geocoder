import requests

from django.conf import settings
from geojson import Feature, Point, FeatureCollection


REQUEST_ERROR_DATA = {
        "data":'API indisponível no momento', 
        "status_code": 404
}

def transform_request(json, scg=1, search_type="search"):
    """
    Função para transformar requisição em geojson

    Argumentos:
        @json (object): dado em formato json para parse
        @scg (int): Ordem de coordenadas geograficas para a aplicação
            1 -> lon, lat
            2 -> lat, lon

    Returns:
        @featureCollection (object): coleção de dados em formato geojson
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

    else:
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

    return {"data": FeatureCollection({
        'Erro de geocodificação, ponto sem informação'
        }) , "status_code": 200 }


def request_search_data(query, scg=1, url=settings.NOMINATIM_URL):
    """
    Função para requisição de dados da api de busca do nominatim 

    Argumentos:
        @query: Pesquisa realizada em api Nominatim
        @scg (int): Ordem de coordenadas geograficas para a aplicação
            1 -> lon, lat
            2 -> lat, lon
        @url (str): string de pesquisa do nominatim
    """
    params = {}
    params["q"] = query
    params["format"] = 'json'
    params["polygon"] = 1

    try:
        r = requests.get(url, params=params)
    except Exception:
        return REQUEST_ERROR_DATA

    if r.status_code == 200:
        return transform_request(r.json(), scg, search_type="search")

    return REQUEST_ERROR_DATA

def request_reverse_data(lat, lon, scg=1, url=settings.NOMINATIM_URL_REVERSE):
    """ 
    Função para requisição de dados para a API reversa do nominatim
    Argumentos:
        @lat (float): latitude
        @lon (float): longitude
        @scg (int): Ordem de coordenadas geograficas para a aplicação
            1 -> lon, lat
            2 -> lat, lon
        @url (str): string de pesquisa do nominatim
    """
    params = {}
    params["lat"] = float(lat)
    params["lon"] = float(lon)
    params["format"] = 'json'

    try:
        r = requests.get(url, params=params)
    except Exception:
        return REQUEST_ERROR_DATA

    if r.status_code == 200:
        return transform_request(r.json(), scg, search_type="reverse")

    return REQUEST_ERROR_DATA