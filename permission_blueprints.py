from flask import Blueprint, request
import requests
from utils import load_file_config, HEADERS

permission_blueprints = Blueprint('permission_blueprints', __name__)
data_config = load_file_config()
url_base = data_config.get('url-backend-security') + "/permission"


@permission_blueprints.route("/permissions", methods=['GET'])
def get_all_permissions() -> dict:
    url = url_base + "/all"
    response = requests.get(url, headers=HEADERS)
    return response.json()


@permission_blueprints.route("/permission/<int:id>", methods=['GET'])
def get_permission_by_id(id_: int) -> dict:
    url = url_base + f'/{id_}'
    response = requests.get(url, headers=HEADERS)
    return response.json()


@permission_blueprints.route("/permission/insert", methods=['POST'])
def insert_permission() -> dict:
    permission = request.get_json()
    url = url_base + "/insert"
    response = requests.post(url, headers=HEADERS, json=permission)
    return response.json()


@permission_blueprints.route("/permission/update/<int:id_>", methods=['PUT'])
def update_permission(id_: int) -> dict:
    permission = request.get_json()
    url = url_base + f'/update/{id_}'
    response = requests.patch(url, headers=HEADERS, json=permission)
    return response.json()


@permission_blueprints.route("/permission/delete/<int:id_>", methods=['DELETE'])
def delete_permission(id_: int) -> dict:
    url = url_base + f'/delete/{id_}'
    response = requests.delete(url, headers=HEADERS)
    return response.json()
