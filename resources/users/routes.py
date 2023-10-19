from flask import request
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from schemas import AuthUserSchema, UpdateUserSchema, UserSchema

from . import bp
from .UserModel import UserModel
from app import db
from db import users



@bp.route('/user')
class UserList(MethodView):
    # get all users
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


    # create user
    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel()
        user.from_dict(user_data)
        try:
            user.save()
            return user_data
        except IntegrityError:
            abort(400, message='Username or Email already taken')

    # delete a user
    # @bp.arguments(AuthUserSchema)
    def delete(self):
        user_data = request.get_json()
        user = UserModel.query.filter_by(username=user_data['username']).first()
        if user and user.username == user_data['username'] and user.check_password(user_data['password']):
            user.delete()
            return {'message':f'{user_data["username"]} deleted'}, 202
        abort(400, message='Username or Password Invalid')


@bp.route('/user/<user_id>')
class User(MethodView):
    # get a single user
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id, description='User not found')

    # Edit a user
    @bp.arguments(UpdateUserSchema)
    @bp.response(200, UpdateUserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id, description='User not found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message='Username or Email already taken.')




# Get All Boulders For Individual User
# @bp.get('/user/<user_id>/boulder')
# def get_user_boulders(user_id):
#     if user_id not in users:
#         abort(404, message='User not found')
#     user_boulders = [boulder for boulder in boulders.values() if boulder['user_id'] == user_id]
#     return user_boulders, 200