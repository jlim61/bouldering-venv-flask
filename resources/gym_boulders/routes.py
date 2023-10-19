from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from . import bp
from db import gym_boulders


@bp.route('/gym_boulder')
class GymBoulderList(MethodView):
    # get all boulders
    def get(self):
        return {'boulders': gym_boulders}

    # create boulder
    def post(self):
        gym_boulder_id = request.get_json()
        for k in ['location', 'grade', 'setter']:
            if k not in gym_boulder_id:
                abort(400, message='Please include location, grade, setter')
        gym_boulders[uuid4().hex] = gym_boulder_id
        return gym_boulder_id, 201


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
    def put(self, gym_boulder_id):
        gym_boulder_data = request.get_json()
        try:
            boulder = gym_boulders[gym_boulder_id]
            if 'grade' in gym_boulder_data:
                boulder['grade'] = gym_boulder_data['grade']
            return boulder, 200
        except KeyError:
            abort(404, message='Boulder not found')


    # delete boulder
    def delete(self, gym_boulder_id):
        try:
            deleted_gym_boulder = gym_boulders.pop(gym_boulder_id)
            return {'message': f'{deleted_gym_boulder} deleted'}, 202
        except KeyError:
            abort(404, message='Boulder not found')

