from datetime import timedelta
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token, verify_jwt_in_request,
                                get_jwt_identity)
from waitress import serve
import requests

import utils
from candidate_blueprints import candidate_blueprints


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "team4"
cors = CORS(app)
jwt = JWTManager(app)
app.register_blueprint(candidate_blueprints)


@app.before_request
def before_request_callback():
    endpoint = utils.clear_url(request.path)
    exclude_route = ['/login', '/']
    if exclude_route.__contains__(request.path):
        pass
    elif verify_jwt_in_request():
        user = get_jwt_identity()
        if user.get('rol'):
            has_grant = utils.validate_grant(endpoint, request.method, user['rol'].get('idRol'))
            if not has_grant:
                return {"message": "Permission denied"}, 401
        else:
            return {"message": "Permission denied. Rol is no defined"}, 401


@app.route("/", methods=['GET'])
def home():
    response = {"message": "Wellcome+"}
    return response


@app.route("/login", methods=['POST'])
def login() -> tuple:
    user = request.get_json()
    url = data_config.get("url-backend-security") + "/user/login"
    response = requests.post(url, headers=utils.HEADERS, json=user)
    if response.status_code == 200:
        user_logged = response.json()
        expires = timedelta(days=1)
        access_token = create_access_token(identity=user_logged, expires_delta=expires)
        return {"token": access_token, "user_id": user_logged.get('id')}, 200
    else:
        return {"message": "Access denied"}, 400


if __name__ == '__main__':
    data_config = utils.load_file_config()
    print("API Gateway Server Running: http://" + data_config.get("url-api-gateway") +
          ":" + str(data_config.get("port")))
    serve(app, host=data_config.get("url-api-gateway"), port=data_config.get("port"))


