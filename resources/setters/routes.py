from flask import request
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from schemas import AuthUserSchema, GymBoulderSchema, MoonBoardBoulderSchema, SetterSchema, UpdateSetterSchema

from . import bp
from .SetterModel import SetterModel
from app import db
from db import setters, gym_boulders, moonboard_boulders



@bp.route('/setter')
class SetterList(MethodView):
    # get all setters
    @bp.response(200, SetterSchema(many=True))
    def get(self):
        return SetterModel.query.all()


    # create a setter
    @bp.arguments(SetterSchema)
    @bp.response(201, SetterSchema)
    def post(self, setter_data):
        setter = SetterModel()
        setter.from_dict(setter_data)
        try:
            setter.save()
            return setter_data
        except IntegrityError:
            abort(400, message='Username or Email already taken')

    # delete a user
    # @bp.arguments(AuthUserSchema)
    def delete(self):
        setter_data = request.get_json()
        setter = SetterModel.query.filter_by(username=setter_data['username']).first()
        if setter and setter.username == setter_data['username'] and setter.check_password(setter_data['password']):
            setter.delete()
            return {'message':f'{setter_data["username"]} deleted'}, 202
        abort(400, message='Username or Password Invalid')


@bp.route('/setter/<setter_id>')
class Setter(MethodView):
    # get a single setter
    @bp.response(200, SetterSchema)
    def get(self, setter_id):
        return SetterModel.query.get_or_404(setter_id, description='Setter not found')


    # Edit a setter
    @bp.arguments(UpdateSetterSchema)
    @bp.response(200, UpdateSetterSchema)
    def put(self, setter_data, setter_id):
        setter = SetterModel.query.get_or_404(setter_id, description='setter not found')
        if setter and setter.check_password(setter_data['password']):
            try:
                setter.from_dict(setter_data)
                setter.save()
                return setter
            except IntegrityError:
                abort(400, message='Username or Email already taken.')

# Get All Gym Boulders For Individual Setter
@bp.get('/user/<setter_id>/gym_boulder')
@bp.response(200, GymBoulderSchema(many=True))
def get_setter_boulders(setter_id):
    if setter_id not in setters:
        abort(404, message='setter not found')
    setter_gym_boulders = [gym_boulder for gym_boulder in gym_boulders.values() if gym_boulder['setter_id'] == setter_id]
    setter_moonboard_boulders = [moonboard_boulder for moonboard_boulder in moonboard_boulders.values() if moonboard_boulder['setter_id'] == setter_id]
    return setter_gym_boulders, setter_moonboard_boulders

# Get All Moonboard Boulders For Individual Setter
@bp.get('/user/<setter_id>/moonboard_boulder')
@bp.response(200, MoonBoardBoulderSchema(many=True))
def get_setter_boulders(setter_id):
    if setter_id not in setters:
        abort(404, message='setter not found')
    setter_moonboard_boulders = [moonboard_boulder for moonboard_boulder in moonboard_boulders.values() if moonboard_boulder['setter_id'] == setter_id]
    return setter_moonboard_boulders