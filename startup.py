import mongoengine

from pathlib import Path
from flask_restx import Api
from flask import Flask, Blueprint
from utils.yaml_reader import read_yaml
from docs.hello_doc import hello_namespace
from controllers.users_controller import users_bp

config_dict = read_yaml(Path('config.yaml'))
app = Flask(__name__)

mongoengine.connect(host=config_dict["database"]["url"])
base_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(base_bp, version='1.0', title='TodoMVC API',
	description='A simple TodoMVC API'
)
api.add_namespace(hello_namespace)
base_bp.register_blueprint(users_bp)
app.register_blueprint(base_bp)

if __name__ == '__main__':
	app.run(debug=True)