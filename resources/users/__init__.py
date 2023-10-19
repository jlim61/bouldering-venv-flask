from flask_smorest import Blueprint

bp =Blueprint('users', __name__, description='Ops on users')

from . import routes