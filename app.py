from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
from docs.hello_doc import hello_namespace 
from controllers.hello_controller import hello_bp

app = Flask(__name__)

base_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(base_bp, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API'
)

api.add_namespace(hello_namespace)

base_bp.register_blueprint(hello_bp)
app.register_blueprint(base_bp)

if __name__ == '__main__':
	app.run(debug=True)