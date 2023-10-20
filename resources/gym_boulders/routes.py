from flask import request
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from resources.setters.SetterModel import SetterModel

from . GymBoulderModel import GymBoulderModel
from schemas import GymBoulderSchema, UpdateGymBoulderSchema
from . import bp


@bp.route('/gym_boulder')
class GymBoulderList(MethodView):
    # get all boulders
    @bp.response(200, GymBoulderSchema(many=True))
    def get(self):
        return GymBoulderModel.query.all()

    # create boulder
    @bp.arguments(GymBoulderSchema)
    @bp.response(200, GymBoulderSchema)
    def post(self, gym_boulder_data):
        gb = GymBoulderModel(**gym_boulder_data)
        sid = SetterModel.query.get(gym_boulder_data['setter_id'])
        if sid:
            gb.save()
            return gb
        else:
            abort(400, message='Invalid Setter ID')


@bp.route('/gym_boulder/<gym_boulder_id>')
class GymBoulder(MethodView):
    # get a single boulder
    @bp.arguments(GymBoulderSchema)
    @bp.response(200, GymBoulderSchema)
    def get(self, gym_boulder_id):
        gb = GymBoulderModel.query.get(gym_boulder_id)
        if gb:
            return gb
        else:
            abort(404, message='Boulder not found')

    # edit boulder
    @bp.arguments(UpdateGymBoulderSchema)
    @bp.response(200, GymBoulderSchema)
    def put(self, gym_boulder_data, gym_boulder_id):
        gb = GymBoulderModel.query.get(gym_boulder_id)
        if gb is None:
            abort(404, message='Boulder not found')
        if gb:
            if gb.setter_id == gym_boulder_data['setter_id']:
                for key, value in gym_boulder_data.items():
                    if value is not None:
                        setattr(gb, key, value)
                gb.save()
                return gb
        abort(400, message="Cannot edit another setter's boulder")



    # delete boulder
    def delete(self, gym_boulder_id):
        request_data = request.get_json()
        setter_id = request_data['setter_id']
        gb = GymBoulderModel.query.get(gym_boulder_id)
        if gb:
            if gb.setter_id == setter_id:
                gb.delete()
                return {'message': 'Boulder Deleted'}, 200
            abort(400, message='Cannot delete other setter\'s boulder')
        abort(400, message='Invalid Boulder ID')

