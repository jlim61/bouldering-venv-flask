from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from resources.users.UserModel import UserModel

from . GymBoulderModel import GymBoulderModel
from schemas import GymBoulderSchema, UpdateGymBoulderSchema
from . import bp


@bp.route('/gym_boulder')
class GymBoulderList(MethodView):
    # get all boulders
    @jwt_required()
    @bp.response(200, GymBoulderSchema(many=True))
    def get(self):
        return GymBoulderModel.query.all()

    # create boulder
    @jwt_required()
    @bp.arguments(GymBoulderSchema)
    @bp.response(200, GymBoulderSchema)
    def post(self, gym_boulder_data):
        setter_id = get_jwt_identity()
        gb = GymBoulderModel(**gym_boulder_data, setter_id = setter_id)
        try:
            gb.save()
            return gb
        except IntegrityError:
            abort(400, message='Invalid Setter ID')


@bp.route('/gym_boulder/<gym_boulder_id>')
class GymBoulder(MethodView):
    # get a single boulder
    @jwt_required()
    @bp.response(200, GymBoulderSchema)
    def get(self, gym_boulder_id):
        gb = GymBoulderModel.query.get(gym_boulder_id)
        if gb:
            return gb
        else:
            abort(404, message='Boulder not found')

    # edit boulder
    @jwt_required()
    @bp.arguments(UpdateGymBoulderSchema)
    @bp.response(200, GymBoulderSchema)
    def put(self, gym_boulder_data, gym_boulder_id):
        gb = GymBoulderModel.query.get(gym_boulder_id)
        if gb is None:
            abort(404, message='Boulder not found')
        if gb:
            setter_id = get_jwt_identity()
            if gb.setter_id == setter_id:
                for key, value in gym_boulder_data.items():
                    if value is not None:
                        setattr(gb, key, value)
                gb.save()
                return gb
            else:
                abort(400, message="Cannot edit another setter's boulder")
        abort(400, message="Invalid Boulder Data")



    # delete boulder
    @jwt_required()
    def delete(self, gym_boulder_id):
        setter_id = get_jwt_identity()
        gb = GymBoulderModel.query.get(gym_boulder_id)
        if gb:
            if gb.setter_id == setter_id:
                gb.delete()
                return {'message': 'Boulder Deleted'}, 200
            abort(400, message='Cannot delete other setter\'s boulder')
        abort(400, message='Invalid Boulder ID')

