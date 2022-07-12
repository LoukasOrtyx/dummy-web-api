from flask import Blueprint

hello_bp = Blueprint('home', __name__, url_prefix='/hello')

@hello_bp.route('/')
def hello_world():
	return 'Hello, World!'
