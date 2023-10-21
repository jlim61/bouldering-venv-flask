from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from resources.gym_boulders.GymBoulderModel import GymBoulderModel
from resources.moonboard_boulders.MoonboardBoulderModel import MoonboardBoulderModel
from resources.users.UserModel import UserModel

from schemas import AllBoulderSchema, AuthUserSchema, GymBoulderSchema, MoonBoardBoulderSchema, UserSchemaNested, UserSetterSchema, UpdateUserSetterSchema

from . import bp
from app import db
from db import setters, gym_boulders, moonboard_boulders



@bp.route('/setter')
class SetterList(MethodView):
    # get all setters
    @bp.response(200, UserSetterSchema(many=True))
    def get(self):
        return UserModel.query.filter_by(setter=True).all()
    
    # delete a setter
    @jwt_required()
    @bp.arguments(AuthUserSchema)
    def delete(self, user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        if user and user.username == user_data['username'] and user.check_password(user_data['password']):
            user.delete()
            return {'message':f'{user_data["username"]} deleted'}, 202
        abort(400, message='Username or Password Invalid')

    # Edit a setter
    @jwt_required()
    @bp.arguments(UpdateUserSetterSchema)
    @bp.response(200, UpdateUserSetterSchema)
    def put(self, setter_data):
        setter_id = get_jwt_identity()
        setter = UserModel.query.get_or_404(setter_id, description='setter not found')
        if setter and setter.check_password(setter_data['password']):
            try:
                setter.from_dict(setter_data)
                setter.save()
                return setter
            except IntegrityError:
                abort(400, message='Username or Email already taken.')

@bp.route('/setter/<setter_id>')
class Setter(MethodView):
    # get a single setter
    @bp.response(200, UserSchemaNested)
    def get(self, setter_id):
        setter = None
        if setter_id.isdigit():
            setter = UserModel.query.get(setter_id)
        if not setter:
            setter = UserModel.query.filter_by(username=setter_id).first()
        if setter:
            return setter
        abort(400, message='Please enter valid username or id')



# Get All Boulders For Individual Setter
@bp.get('/user/<setter_id>/gym_boulder')
@bp.response(200, AllBoulderSchema)
def get_setter_boulders(setter_id):
    setter = UserModel.query.get(setter_id)
    if not setter:
        abort(404, message='setter not found')
    gym_boulders = GymBoulderModel.query.filter_by(setter_id=setter_id).all()
    moonboard_boulders = MoonboardBoulderModel.query.filter_by(setter_id=setter_id).all()
    all_boulders = {
        'gym_boulders': GymBoulderSchema(many=True).dump(gym_boulders),
        'moonboard_boulders': MoonBoardBoulderSchema(many=True).dump(moonboard_boulders),
    }
    return all_boulders