from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from schemas import MoonBoardBoulderSchema, UpdateMoonBoardBoulderSchema

from . import bp
from db import moonboard_boulders


@bp.route('/moonboard_boulder')
class MoonboardBoulderList(MethodView):
    # get boulder
    def get(self):
        return {'boulders': moonboard_boulders}

    # create boulder
    @bp.arguments(MoonBoardBoulderSchema)
    def post(self, moonboard_boulder_data):
        moonboard_boulders[uuid4().hex] = moonboard_boulder_data
        return moonboard_boulder_data, 201


@bp.route('/moonboard_boulder/<moonboard_boulder_id>')
class MoonboardBoulder(MethodView):
    # get a single boulder
    def get(self, moonboard_boulder_id):
        try:
            boulder = moonboard_boulders[moonboard_boulder_id]
            return boulder, 200
        except KeyError:
            abort(404, message='Boulder not found')
            # return {'message': 'boulder not found'}, 404

    # edit boulder
    @bp.arguments(UpdateMoonBoardBoulderSchema)
    def put(self, moonboard_boulder_data, moonboard_boulder_id):
        if moonboard_boulder_id in moonboard_boulders:
            moonboard_boulder = moonboard_boulders[moonboard_boulder_id]
            if moonboard_boulder_data['setter_id'] != moonboard_boulder['setter_id']:
                abort(400, message="Cannot edit another setter's boulder")
            for key, value in moonboard_boulder_data.items():
                if value is not None:
                    moonboard_boulder[key] = value
        return moonboard_boulder, 200

    # delete boulder
    def delete(self, moonboard_boulder_id):
        try:
            deleted_moonboard_boulder = moonboard_boulders.pop(moonboard_boulder_id)
            return {'message': f'{deleted_moonboard_boulder} deleted'}, 202
        except KeyError:
            abort(404, message='Boulder not found')

