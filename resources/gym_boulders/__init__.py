from flask_smorest import Blueprint

bp = Blueprint('gym_boulders', __name__, description='Ops on gym boulders')

from . import routes