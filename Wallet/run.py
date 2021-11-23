from flask import Flask, request
from api.v1 import routes as api_v1
from api.v2 import routes as api_v2

api = Flask(__name__)

# Version blueprints
api.register_blueprint(api_v1, url_prefix='/v1')
api.register_blueprint(api_v2, url_prefix='/v2')

api.run(debug=True)