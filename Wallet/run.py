from flask import Flask, request
from api.v1 import routes as api_v1
from api.v2 import routes as api_v2

app = Flask(__name__)

# Version blueprints
app.register_blueprint(api_v1.api, url_prefix='/v1')
app.register_blueprint(api_v2.api, url_prefix='/v2')

app.run(debug=True)