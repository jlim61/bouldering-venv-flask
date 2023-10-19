from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from . import bp
from db import moonboard_boulders


@bp.route('/moonboard_boulder')
class MoonboardBoulderList(MethodView):
    # get boulder
    def get(self):
        return {'boulders': moonboard_boulders}

    # create boulder
    def post(self):
        moonboard_boulder_id = request.get_json()
        for k in ['boulder_name', 'grade', 'setter', 'starting_hold', 'usable_holds', 'finish_hold', 'moonboard_configuration']:
            if k not in moonboard_boulder_id:
                abort(400, message='Please include boulder_name, grade, setter, starting_hold, usable_holds, finish_hold, and moonboard_configuration')
        moonboard_boulders[uuid4().hex] = moonboard_boulder_id
        return moonboard_boulder_id, 201


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
    def put(self, moonboard_boulder_id):
        moonboard_boulder_data = request.get_json()
        try:
            boulder = moonboard_boulders[moonboard_boulder_id]
            boulder['grade'] = moonboard_boulder_data['grade']
            return boulder, 200
        except KeyError:
            abort(404, message='Boulder not found')

    # delete boulder
    def delete(self, moonboard_boulder_id):
        try:
            deleted_moonboard_boulder = moonboard_boulders.pop(moonboard_boulder_id)
            return {'message': f'{deleted_moonboard_boulder} deleted'}, 202
        except KeyError:
            abort(404, message='Boulder not found')

