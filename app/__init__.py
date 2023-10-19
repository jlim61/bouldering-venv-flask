from flask import Flask
from flask_smorest import Api
from Config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

from resources.users import bp as user_bp
api.register_blueprint(user_bp)
from resources.setters import bp as setter_bp
api.register_blueprint(setter_bp)
from resources.gym_boulders import bp as gym_boulder_bp
api.register_blueprint(gym_boulder_bp)
from resources.moonboard_boulders import bp as moonboard_boulder_bp
api.register_blueprint(moonboard_boulder_bp)

from resources.users import routes
from resources.setters import routes
from resources.gym_boulders import routes
from resources.moonboard_boulders import routes