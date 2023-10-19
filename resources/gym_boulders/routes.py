from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from schemas import GymBoulderSchema, UpdateGymBoulderSchema
from . import bp
from db import gym_boulders


@bp.route('/gym_boulder')
class GymBoulderList(MethodView):
    # get all boulders
    def get(self):
        return {'boulders': gym_boulders}

    # create boulder
    @bp.arguments(GymBoulderSchema)
    def post(self, gym_boulder_data):
        gym_boulders[uuid4().hex] = gym_boulder_data
        return gym_boulder_data, 201


@bp.route('/gym_boulder/<gym_boulder_id>')
class GymBoulder(MethodView):
    # get a single boulder
    def get(self, gym_boulder_id):
        try:
            boulder = gym_boulders[gym_boulder_id]
            return boulder, 200
        except KeyError:
            abort(404, message='Boulder not found')
            # return {'message': 'boulder not found'}, 404

    # edit boulder
    @bp.arguments(UpdateGymBoulderSchema)
    def put(self, gym_boulder_data, gym_boulder_id):
        if gym_boulder_id in gym_boulders:
            gym_boulder = gym_boulders[gym_boulder_id]
            if gym_boulder_data['setter_id'] != gym_boulder['setter_id']:
                abort(400, message="Cannot edit another setter's boulder")
            for key, value in gym_boulder_data.items():
                if value is not None:
                    gym_boulder[key] = value
        return gym_boulder, 200


    # delete boulder
    def delete(self, gym_boulder_id):
        try:
            deleted_gym_boulder = gym_boulders.pop(gym_boulder_id)
            return {'message': f'{deleted_gym_boulder} deleted'}, 202
        except KeyError:
            abort(404, message='Boulder not found')

