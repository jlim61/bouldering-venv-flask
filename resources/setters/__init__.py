from flask_smorest import Blueprint

bp =Blueprint('setters', __name__, description='Ops on setters')

from . import routes