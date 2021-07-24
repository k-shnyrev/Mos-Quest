import sys

import requests

geocoder_api_server = 'https://geocode-maps.yandex.ru/1.x/'
geocoder_api_key = '...'  # получите ключ для Геокодера API Яндекс.Карт - https://yandex.ru/dev/maps/geocoder/
search_api_server = 'https://search-maps.yandex.ru/v1/'
search_api_key = '...'  # получите ключ для API Поиска по организациям Яндекс.Карт - https://yandex.ru/dev/maps/geosearch/
map_api_server = 'https://static-maps.yandex.ru/1.x/'


def check(response):
    if not response:
        print(f'HTTP {response.status_code} {response.reason}')
        print(response.text)
        sys.exit(1)
    else:
        return response


def toponyms_search(toponym_to_find):
    """
    Поиск топонимов по запросу toponym_to_find, возвращает топонимы в формате json
    Первый найденный - toponyms_search(...)[0]['GeoObject']
    """
    geocoder_params = {
        "apikey": geocoder_api_key,
        "geocode": toponym_to_find,
        "format": "json"}
    response = check(requests.get(geocoder_api_server, params=geocoder_params))
    json_response = response.json()
    return json_response['response']['GeoObjectCollection']['featureMember']


def advanced_toponyms_search(geocoder_params):
    """
    Поиск топонимов с параметрами geocoder_params,
    возвращает топонимы в формате json.
    Первый найденный - advanced_toponyms_search(...)[0]['GeoObject']
    """
    geocoder_params['apikey'] = geocoder_api_key
    geocoder_params['format'] = 'json'
    response = check(requests.get(geocoder_api_server, params=geocoder_params))
    json_response = response.json()
    return json_response['response']['GeoObjectCollection']['featureMember']


def find_objects(search_params):
    """
    Поиск объектов с параметрами geocoder_params,
    возвращает объекты в формате json.
    Первый найденный - find_objects(...)[0]
    """
    search_params['apikey'] = search_api_key
    response = check(requests.get(search_api_server, params=search_params))
    json_response = response.json()
    return json_response['features']


def get_map(map_params):
    """
    Принимает map_params - словарь с ключами 'll', 'l', 'z' и другими
    Возвращает изображение - содержимое ответа Yandex.Maps Static API
    """
    return check(requests.get(map_api_server, params=map_params)).content


def save_toponym_map(toponym_title, file_name):
    """
    Сохраняет карту с отметкой в центре toponym_title
    в файл с именем file_name
    """
    toponym = toponyms_search(toponym_title)[0]['GeoObject']
    coords = toponym['Point']['pos'].replace(' ', ',')
    map_params = {
        'll': coords,
        'pt': coords + ',pm2dgm',
        'l': 'map',
        'z': 16
    }
    map_image = get_map(map_params)
    with open(file_name, 'wb') as f:
        f.write(map_image)
