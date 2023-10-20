from flask import request
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from resources.setters.SetterModel import SetterModel
from . MoonboardBoulderModel import MoonboardBoulderModel
from schemas import MoonBoardBoulderSchema, UpdateMoonBoardBoulderSchema
from . import bp


@bp.route('/moonboard_boulder')
class MoonboardBoulderList(MethodView):
    # get all boulders
    @bp.response(200, MoonBoardBoulderSchema(many=True))
    def get(self):
        return MoonboardBoulderModel.query.all()

    # create boulder
    @bp.arguments(MoonBoardBoulderSchema)
    @bp.response(200, MoonBoardBoulderSchema)
    def post(self, moonboard_boulder_data):
        mb = MoonboardBoulderModel(**moonboard_boulder_data)
        sid = SetterModel.query.get(moonboard_boulder_data['setter_id'])
        if sid:
            mb.save()
            return mb
        else:
            abort(400, message='Invalid Setter ID')



@bp.route('/moonboard_boulder/<moonboard_boulder_id>')
class MoonboardBoulder(MethodView):
    # get a single boulder
    @bp.arguments(UpdateMoonBoardBoulderSchema)
    @bp.response(200, MoonBoardBoulderSchema)
    def get(self, moonboard_boulder_id):
        mb = MoonboardBoulderModel.query.get(moonboard_boulder_id)
        if mb:
            return mb
        else:
            abort(404, message='Boulder not found')

    # edit boulder
    @bp.arguments(UpdateMoonBoardBoulderSchema)
    @bp.response(200, MoonBoardBoulderSchema)
    def put(self, moonboard_boulder_data, moonboard_boulder_id):
        mb = MoonboardBoulderModel.query.get(moonboard_boulder_id)
        if mb is None:
            abort(404, message='Boulder not found')
        if mb:
            if mb.setter_id == moonboard_boulder_data['setter_id']:
                for key, value in moonboard_boulder_data.items():
                    if value is not None:
                        setattr(mb, key, value)
                mb.save()
                return mb
        abort(400, message="Cannot edit another setter's boulder")


    # delete boulder
    def delete(self, moonboard_boulder_id):
        request_data = request.get_json()
        setter_id = request_data['setter_id']
        mb = MoonboardBoulderModel.query.get(moonboard_boulder_id)
        if mb:
            if mb.setter_id == setter_id:
                mb.delete()
                return {'message': 'Boulder Deleted'}, 200
            abort(400, message='Cannot delete other setter\'s boulder')
        abort(400, message='Invalid Boulder ID')
