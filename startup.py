import mongoengine

from pathlib import Path
from flask_restx import Api
from flask import Flask, Blueprint
from utils.yaml_reader import read_yaml
from controllers.user_controller import api as user_ns

config_dict = read_yaml(Path('config.yaml'))

mongoengine.connect(host=config_dict["database"]["url"])
base_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(base_bp, version='1.0', title='Dummy Web API',
	description='A simple user Web API with CRUD and JWT Auth'
)
api.add_namespace(user_ns, path='/users')

app = Flask(__name__)
app.register_blueprint(base_bp)

if __name__ == '__main__':
	app.run(debug=True)