from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from schemas import SetterSchema, UpdateSetterSchema

from . import bp
from db import setters



@bp.route('/setter')
class SetterList(MethodView):
    # get all setters
    @bp.response(200, SetterSchema(many=True))
    def get(self):
        return setters.values()


    # create a setter
    @bp.arguments(SetterSchema)
    @bp.response(201, SetterSchema)
    def post(self, setter_data):
        setters[uuid4().hex] = setter_data
        return setter_data


@bp.route('/setter/<setter_id>')
class Setter(MethodView):
    # get a single setter
    def get(self, setter_id):
        try:
            setter = setters[setter_id]
            return setter, 200
        except KeyError:
            abort(404, message='setter not found')

    # Edit a setter
    @bp.arguments(UpdateSetterSchema)
    def put(self, setter_data, setter_id):
        if setter_id in setters:
            setter = setters[setter_id]
            if 'password' in setter_data and setter_data['password'] != setter['password']:
                abort(404, message='Incorrect Password')
            for key, value in setter_data.items():
                if value is not None:
                    if key == 'password':
                        if 'new_password' in setter_data:
                            setter['password'] = setter_data['new_password']
                        else:
                            setter['password'] = value
                    else:
                        setter[key] = value
            return setter, 200

    # delete a setter
    def delete(self, setter_id):
        try:
            deleted_setter = setters.pop(setter_id)
            return {'message': f'{deleted_setter["username"]} deleted'}, 202
        except:
            abort(404, message='setter not found')