import json
import re

import requests

HEADERS = {"Content-Type": "application/json; charset=utf-8"}


def load_file_config():
    """
    Convert the connection data from json to a dictionary
    Configurate and execute the app
    :return: Python dictionary
    """
    with open("config.json", "r") as file_:
        data = json.load(file_)
    return data


def clear_url(url: str) -> str:
    """
    All alpha numbers are get as a ? just to validate if the user are granted
    :param url: url
    :return: url
    """
    segments = url.split('/')
    for segment in segments:
        if re.search('\\d', segment):
            url = url.replace(segment, "?")
    return url


def validate_grant(endpoint: str, method: str, id_rol: int):
    """
    Connect with the security backend and validate a permission
    :param endpoint:
    :param method:
    :param id_rol:
    :return: Rol are granted
    """
    data_config = load_file_config()
    url = data_config.get('url-backend-security') + f'/rol/validate/{id_rol}'
    body = {
        "url": endpoint,
        "method": method
    }
    response = requests.get(url, headers=HEADERS, json=body)
    has_grant = False
    try:
        if response.status_code == 200:
            has_grant = True
    except Exception as e:
        print(e)
    return has_grant
