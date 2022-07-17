from flask_restx import Namespace, fields

def _response(self, code, description, model=None, **kwargs):
    """
    A decorator to specify one of the expected responses

    :param int code: the HTTP status code
    :param str description: a small description about the response
    :param ModelBase model: an optional response model

    """
    return self.doc(responses={int(code): (description, model, kwargs)})

Namespace.response = _response