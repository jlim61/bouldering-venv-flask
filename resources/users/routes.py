from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from schemas import UpdateUserSchema, UserSchema

from . import bp
from db import users



@bp.route('/user')
class UserList(MethodView):
    # get all users
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return users.values()


    # create a user
    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        users[uuid4().hex] = user_data
        return user_data


@bp.route('/user/<user_id>')
class User(MethodView):
    # get a single user
    def get(self, user_id):
        try:
            user = users[user_id]
            return user, 200
        except KeyError:
            abort(404, message='User not found')

    # Edit a user
    @bp.arguments(UpdateUserSchema)
    def put(self, user_data, user_id):
        if user_id in users:
            user = users[user_id]
            if 'password' in user_data and user_data['password'] != user['password']:
                abort(404, message='Incorrect Password')
            for key, value in user_data.items():
                if value is not None:
                    if key == 'password':
                        if 'new_password' in user_data:
                            user['password'] = user_data['new_password']
                        else:
                            user['password'] = value
                    else:
                        user[key] = value
            return user, 200

    # delete a user
    def delete(self, user_id):
        try:
            deleted_user = users.pop(user_id)
            return {'message': f'{deleted_user["username"]} deleted'}, 202
        except:
            abort(404, message='User not found')



# Get All Boulders For Individual User
# @bp.get('/user/<user_id>/boulder')
# def get_user_boulders(user_id):
#     if user_id not in users:
#         abort(404, message='User not found')
#     user_boulders = [boulder for boulder in boulders.values() if boulder['user_id'] == user_id]
#     return user_boulders, 200