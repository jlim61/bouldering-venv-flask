from flask_smorest import Blueprint

bp = Blueprint('moonboard_boulders', __name__, description='Ops on moonboard boulders')

from . import routes